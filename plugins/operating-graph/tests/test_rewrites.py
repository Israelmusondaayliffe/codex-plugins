"""Rewrite proposal, policy, mutation, and versioning contracts."""

from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from scripts.graph_engine.constants import ApprovalStatus, ApprovalSubjectType, RiskLevel
from scripts.graph_engine.events import EventStore
from scripts.graph_engine.models import Approval, Graph, NodeRuntimeState, RuntimeState, RewriteProposal
from scripts.graph_engine.constants import NodeStatus, RunStatus
from scripts.graph_engine.rewrites import (
    ApprovalRequiredError,
    ProhibitedMutationError,
    RewriteEngine,
    RewritePolicyError,
    RewriteValidationError,
    VersionMismatchError,
    apply_operations,
    classify_risk,
    compile_pattern,
)


TIMESTAMP = "2026-07-18T12:00:00Z"


def node(node_id: str, kind: str, *, critical: bool = True, outputs=None, inputs=None) -> dict[str, object]:
    return {
        "id": node_id,
        "kind": kind,
        "label": node_id.title(),
        "purpose": f"Perform {node_id} work.",
        "enabled": True,
        "critical": critical,
        "priority": 50,
        "execution": {"mode": "human" if kind == "authority" else "inline", "skill": None, "modelHint": None},
        "capabilities": [],
        "inputs": inputs or [],
        "outputs": outputs or [],
        "successCriteria": ["Required work is complete."],
        "budget": {"maxAttempts": 2, "workUnits": 2},
        "localLoop": {"enabled": False, "maxIterations": 1, "sequence": [], "stopCondition": "Required work is complete."},
    }


def edge(edge_id: str, source: str, target: str, kind: str, *, required: bool = True, artifact_types=None) -> dict[str, object]:
    return {
        "id": edge_id,
        "source": source,
        "target": target,
        "kind": kind,
        "enabled": True,
        "required": required,
        "temporal": "same_epoch",
        "artifactTypes": artifact_types or [],
        "activation": {"mode": "all", "nodeStates": [], "artifacts": [], "approvals": []},
    }


def graph_data() -> dict[str, object]:
    report = {"artifactType": "report", "required": True}
    return {
        "schemaVersion": "1.0",
        "graphId": "rewrite-test",
        "name": "Rewrite Test",
        "goal": {
            "statement": "Produce a verified report.",
            "deliverables": [{"id": "report", "artifactType": "report", "description": "The report."}],
            "completionCriteria": ["The report exists."],
            "authorityNodeId": "authority",
        },
        "limits": {"maxConcurrentWorkers": 2, "maxNodeRuns": 20, "maxGraphVersions": 6, "maxEpochs": 3, "maxAutoRewrites": 2, "defaultMaxAttempts": 2},
        "nodes": [
            node("authority", "authority"),
            node("controller", "controller"),
            node("producer", "worker", outputs=[report]),
            node("reviewer", "evaluator", inputs=[report]),
            node("optional-helper", "worker", critical=False),
            node("critical-helper", "worker", critical=True),
        ],
        "edges": [
            edge("authority-controller", "authority", "controller", "goal"),
            edge("controller-producer", "controller", "producer", "assign"),
            edge("producer-reviewer", "producer", "reviewer", "verify", artifact_types=["report"]),
            edge("controller-helper", "controller", "optional-helper", "assign", required=False),
            edge("controller-critical-helper", "controller", "critical-helper", "assign", required=False),
        ],
        "rewritePolicy": {"automaticRiskLevels": ["low"], "approvalRiskLevels": ["medium", "high"], "prohibitedMutations": []},
        "metadata": {"createdBy": "tests", "createdAt": TIMESTAMP},
    }


def operation(kind: str, **params: object) -> dict[str, object]:
    return {"kind": kind, "params": params}


def proposal(*operations: dict[str, object], risk: str = "low", base: int = 1) -> RewriteProposal:
    return RewriteProposal.from_dict(
        {
            "proposalId": "rewrite-0001",
            "runId": "run-001",
            "baseGraphVersion": base,
            "trigger": "manual-test",
            "evidenceEventIds": [],
            "riskLevel": risk,
            "reason": "Exercise rewrite behavior.",
            "predictedEffect": "The graph changes within policy.",
            "operations": list(operations),
            "approvalRequired": risk in {"medium", "high"},
            "rollbackVersion": base,
        }
    )


def approval(status: ApprovalStatus = ApprovalStatus.GRANTED) -> Approval:
    return Approval(
        approval_id="approval-0001",
        run_id="run-001",
        subject_type=ApprovalSubjectType.REWRITE,
        subject_id="rewrite-0001",
        requested_by="controller",
        required_from="authority",
        status=status,
        requested_at=TIMESTAMP,
        resolved_at=TIMESTAMP if status != ApprovalStatus.PENDING else None,
        resolved_by="authority" if status != ApprovalStatus.PENDING else None,
    )


class PrimitiveMutationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.graph = Graph.from_dict(graph_data())

    def test_every_primitive_mutation_changes_only_its_declared_target(self) -> None:
        diagnostic = node("diagnostic", "worker", critical=False)
        diagnostic["purpose"] = "Diagnose a bounded failure."
        diagnostic["capabilities"] = ["analysis"]
        new_edge = edge("controller-diagnostic", "controller", "diagnostic", "assign", required=False)
        cases = (
            (operation("add_node", node=diagnostic), lambda data: any(item["id"] == "diagnostic" for item in data["nodes"])),
            (operation("update_node", nodeId="optional-helper", changes={"label": "Optional Diagnostic"}), lambda data: next(item for item in data["nodes"] if item["id"] == "optional-helper")["label"] == "Optional Diagnostic"),
            (operation("disable_node", nodeId="optional-helper"), lambda data: not next(item for item in data["nodes"] if item["id"] == "optional-helper")["enabled"]),
            (operation("add_edge", edge=new_edge), lambda data: any(item["id"] == "controller-diagnostic" for item in data["edges"])),
            (operation("disable_edge", edgeId="controller-helper"), lambda data: not next(item for item in data["edges"] if item["id"] == "controller-helper")["enabled"]),
            (operation("set_priority", nodeId="optional-helper", priority=91), lambda data: next(item for item in data["nodes"] if item["id"] == "optional-helper")["priority"] == 91),
        )
        for item, assertion in cases:
            with self.subTest(kind=item["kind"]):
                rewritten = apply_operations(self.graph, [item])
                self.assertTrue(assertion(rewritten.to_dict()))
                self.assertEqual(rewritten.goal.to_dict(), self.graph.goal.to_dict())

    def test_unknown_targets_and_duplicate_additions_are_rejected(self) -> None:
        duplicate = node("producer", "worker")
        for item, message in (
            (operation("update_node", nodeId="missing", changes={"label": "Missing"}), "unknown node"),
            (operation("disable_edge", edgeId="missing"), "unknown edge"),
            (operation("add_node", node=duplicate), "duplicate node"),
        ):
            with self.subTest(kind=item["kind"]), self.assertRaisesRegex(RewritePolicyError, message):
                apply_operations(self.graph, [item])


class PolicyAndCompilerTests(unittest.TestCase):
    def setUp(self) -> None:
        self.graph = Graph.from_dict(graph_data())

    def test_risk_classification_covers_low_medium_and_high_changes(self) -> None:
        external = node("publisher", "distributor")
        external["execution"]["mode"] = "tool"
        external["capabilities"] = ["publish"]
        self.assertEqual(classify_risk(self.graph, [operation("set_priority", nodeId="producer", priority=70)]), RiskLevel.LOW)
        self.assertEqual(classify_risk(self.graph, [operation("add_node", node=node("alternate", "worker"))]), RiskLevel.MEDIUM)
        self.assertEqual(classify_risk(self.graph, [operation("add_node", node=external)]), RiskLevel.HIGH)
        self.assertEqual(classify_risk(self.graph, [operation("disable_node", nodeId="producer")]), RiskLevel.HIGH)

    def test_prohibited_mutations_are_rejected_even_with_approval(self) -> None:
        prohibited = (
            operation("update_node", nodeId="producer", changes={"capabilities": ["network-write"]}),
            operation("update_node", nodeId="authority", changes={"purpose": "Replace original authority."}),
            operation("disable_edge", edgeId="authority-controller"),
        )
        for item in prohibited:
            with self.subTest(item=item), self.assertRaises(ProhibitedMutationError):
                apply_operations(self.graph, [item])

    def test_critical_nodes_cannot_be_downgraded_to_evade_protection(self) -> None:
        with self.assertRaisesRegex(ProhibitedMutationError, "critical protection"):
            apply_operations(
                self.graph,
                [operation("update_node", nodeId="producer", changes={"critical": False})],
            )

    def test_higher_level_patterns_compile_only_to_primitive_operations(self) -> None:
        arguments = {
            "split_node": {"nodeId": "producer", "nodes": [node("producer-a", "worker"), node("producer-b", "worker")], "edges": []},
            "merge_nodes": {"nodeIds": ["producer", "optional-helper"], "node": node("merged-worker", "worker"), "edges": []},
            "replace_node": {"nodeId": "producer", "node": node("alternate", "worker"), "edges": []},
            "add_reviewer": {"node": node("reviewer-two", "evaluator", critical=False), "edge": edge("producer-reviewer-two", "producer", "reviewer-two", "verify", required=False, artifact_types=["report"])},
            "reroute_edge": {"edgeId": "controller-helper", "edge": edge("producer-helper", "producer", "optional-helper", "assign", required=False)},
            "collapse_fanout": {"edgeIds": ["controller-helper"], "nodeIds": ["optional-helper"]},
            "serialize_branch": {"edge": edge("producer-helper-order", "producer", "optional-helper", "assign", required=False)},
            "create_arbitration_node": {"node": node("arbitrator", "evaluator", critical=False), "edges": [edge("producer-arbitrator", "producer", "arbitrator", "verify", required=False, artifact_types=["report"])]},
            "promote_successful_pattern": {"nodeId": "optional-helper", "priority": 80},
        }
        primitives = {"add_node", "update_node", "disable_node", "add_edge", "disable_edge", "set_priority"}
        for pattern, params in arguments.items():
            with self.subTest(pattern=pattern):
                compiled = compile_pattern(pattern, params)
                self.assertTrue(compiled)
                self.assertTrue(all(item.kind.value in primitives for item in compiled))


class RewriteEngineTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.run_directory = Path(self.temporary.name)
        self.graph = Graph.from_dict(graph_data())
        state = RuntimeState(
            run_id="run-001",
            graph_id=self.graph.graph_id,
            graph_version=1,
            epoch=1,
            status=RunStatus.RUNNING,
            node_states={node.id: NodeRuntimeState(node.id, NodeStatus.PENDING) for node in self.graph.nodes},
        )
        self.engine = RewriteEngine.initialize(self.run_directory, self.graph, state, timestamp=TIMESTAMP)

    def test_version_mismatch_is_rejected(self) -> None:
        item = proposal(operation("set_priority", nodeId="producer", priority=70), base=2)
        with self.assertRaisesRegex(VersionMismatchError, "base graph version 2 does not match current version 1"):
            self.engine.propose(item, timestamp=TIMESTAMP)

    def test_low_risk_rewrite_is_applied_automatically_and_bounded(self) -> None:
        item = proposal(operation("set_priority", nodeId="producer", priority=70))
        self.engine.propose(item, timestamp=TIMESTAMP)
        result = self.engine.apply(item.proposal_id, timestamp=TIMESTAMP)

        self.assertEqual(result.graph_version, 2)
        self.assertEqual(result.auto_rewrites_applied, 1)
        current = json.loads((self.run_directory / "graph.json").read_text())
        self.assertEqual(next(node for node in current["nodes"] if node["id"] == "producer")["priority"], 70)

    def test_medium_and_high_risk_rewrites_require_a_matching_granted_approval(self) -> None:
        for risk, items in (
            (
                "medium",
                (
                    operation("add_node", node=node("alternate", "worker")),
                    operation("add_edge", edge=edge("controller-alternate", "controller", "alternate", "assign")),
                ),
            ),
            ("high", (operation("disable_node", nodeId="critical-helper"),)),
        ):
            with self.subTest(risk=risk):
                with TemporaryDirectory() as directory:
                    state = RuntimeState("run-001", self.graph.graph_id, 1, 1, RunStatus.RUNNING, {node.id: NodeRuntimeState(node.id, NodeStatus.PENDING) for node in self.graph.nodes})
                    engine = RewriteEngine.initialize(Path(directory), self.graph, state, timestamp=TIMESTAMP)
                    candidate = proposal(*items, risk=risk)
                    engine.propose(candidate, timestamp=TIMESTAMP)
                    with self.assertRaises(ApprovalRequiredError):
                        engine.apply(candidate.proposal_id, approvals=[], timestamp=TIMESTAMP)
                    engine.apply(candidate.proposal_id, approvals=[approval()], timestamp=TIMESTAMP)

    def test_declared_risk_cannot_understate_the_classified_risk(self) -> None:
        item = proposal(operation("add_node", node=node("alternate", "worker")), risk="low")
        with self.assertRaisesRegex(RewritePolicyError, "declared risk low understates classified risk medium"):
            self.engine.propose(item, timestamp=TIMESTAMP)

    def test_started_optional_node_is_not_eligible_for_low_risk_automatic_disable(self) -> None:
        state = RuntimeState(
            "run-001",
            self.graph.graph_id,
            1,
            1,
            RunStatus.RUNNING,
            {
                node.id: NodeRuntimeState(
                    node.id,
                    NodeStatus.RUNNING if node.id == "optional-helper" else NodeStatus.PENDING,
                    attempts=1 if node.id == "optional-helper" else 0,
                )
                for node in self.graph.nodes
            },
        )
        with TemporaryDirectory() as directory:
            engine = RewriteEngine.initialize(Path(directory), self.graph, state, timestamp=TIMESTAMP)
            item = proposal(operation("disable_node", nodeId="optional-helper"), risk="low")

            with self.assertRaisesRegex(RewritePolicyError, "understates classified risk medium"):
                engine.propose(item, timestamp=TIMESTAMP)

    def test_applied_rewrite_revalidates_and_rejects_an_invalid_graph(self) -> None:
        item = proposal(operation("disable_node", nodeId="reviewer"), risk="high")
        self.engine.propose(item, timestamp=TIMESTAMP)
        with self.assertRaisesRegex(RewriteValidationError, "OGI-10"):
            self.engine.apply(item.proposal_id, approvals=[approval()], timestamp=TIMESTAMP)
        self.assertFalse((self.run_directory / "graph-versions" / "v0002.json").exists())

    def test_graph_versions_are_immutable_and_applied_record_has_rollback_metadata(self) -> None:
        original = (self.run_directory / "graph-versions" / "v0001.json").read_bytes()
        item = proposal(operation("set_priority", nodeId="producer", priority=70))
        self.engine.propose(item, timestamp=TIMESTAMP)
        self.engine.apply(item.proposal_id, timestamp=TIMESTAMP)

        self.assertEqual((self.run_directory / "graph-versions" / "v0001.json").read_bytes(), original)
        self.assertTrue((self.run_directory / "graph-versions" / "v0002.json").exists())
        applied = json.loads((self.run_directory / "rewrites" / "applied" / "rewrite-0001.json").read_text())
        self.assertEqual(applied["rollbackVersion"], 1)
        self.assertEqual(applied["appliedGraphVersion"], 2)
        self.assertEqual(EventStore(self.run_directory, "run-001").read_all()[-1].type.value, "rewrite.applied")


if __name__ == "__main__":
    unittest.main()
