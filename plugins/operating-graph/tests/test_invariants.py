"""Executable coverage for all 22 Operating Graph invariants."""

from __future__ import annotations

from copy import deepcopy
import hashlib
import json
from pathlib import Path
import tempfile
import unittest

from scripts.graph_engine.invariants import (
    validate_applied_rewrite,
    validate_artifact_path,
    validate_graph_invariants,
    validate_graph_versions,
    validate_runtime_dependencies,
    validate_runtime_limits,
)
from scripts.graph_engine.models import Artifact, Graph, RewriteProposal, RuntimeState
from scripts.graph_engine.validation import parse_and_validate_graph, validate_rewritten_graph


TIMESTAMP = "2026-07-18T12:00:00Z"


def node(
    node_id: str,
    kind: str,
    *,
    inputs: list[dict[str, object]] | None = None,
    outputs: list[dict[str, object]] | None = None,
    capabilities: list[str] | None = None,
) -> dict[str, object]:
    return {
        "id": node_id,
        "kind": kind,
        "label": node_id.title(),
        "purpose": f"Perform {node_id} work.",
        "enabled": True,
        "critical": True,
        "priority": 50,
        "execution": {"mode": "human" if kind == "authority" else "inline", "skill": None, "modelHint": None},
        "capabilities": capabilities or [],
        "inputs": inputs or [],
        "outputs": outputs or [],
        "successCriteria": ["Required work is complete."],
        "budget": {"maxAttempts": 2, "workUnits": 2},
        "localLoop": {
            "enabled": False,
            "maxIterations": 1,
            "sequence": [],
            "stopCondition": "Required work is complete.",
        },
    }


def edge(
    edge_id: str,
    source: str,
    target: str,
    kind: str,
    *,
    temporal: str = "same_epoch",
    artifact_types: list[str] | None = None,
    required: bool = True,
) -> dict[str, object]:
    return {
        "id": edge_id,
        "source": source,
        "target": target,
        "kind": kind,
        "enabled": True,
        "required": required,
        "temporal": temporal,
        "artifactTypes": artifact_types or [],
        "activation": {"mode": "all", "nodeStates": [], "artifacts": [], "approvals": []},
    }


def valid_graph_data() -> dict[str, object]:
    report = {"artifactType": "report", "required": True}
    return {
        "schemaVersion": "1.0",
        "graphId": "verified-report",
        "name": "Verified Report",
        "goal": {
            "statement": "Produce a verified report.",
            "deliverables": [{"id": "final-report", "artifactType": "report", "description": "The report."}],
            "completionCriteria": ["The report exists.", "The evaluator approves it."],
            "authorityNodeId": "human-authority",
        },
        "limits": {
            "maxConcurrentWorkers": 2,
            "maxNodeRuns": 20,
            "maxGraphVersions": 10,
            "maxEpochs": 3,
            "maxAutoRewrites": 2,
            "defaultMaxAttempts": 2,
        },
        "nodes": [
            node("human-authority", "authority"),
            node("controller", "controller"),
            node("producer", "worker", outputs=[report]),
            node("evaluator", "evaluator", inputs=[report]),
            node("publisher", "distributor", inputs=[report], capabilities=["external-side-effect"]),
        ],
        "edges": [
            edge("authority-to-controller", "human-authority", "controller", "goal"),
            edge("controller-to-producer", "controller", "producer", "assign"),
            edge("producer-to-evaluator", "producer", "evaluator", "verify", artifact_types=["report"]),
            edge("producer-to-publisher", "producer", "publisher", "write", artifact_types=["report"]),
            edge("authority-to-publisher", "human-authority", "publisher", "approve"),
        ],
        "rewritePolicy": {
            "automaticRiskLevels": ["low"],
            "approvalRiskLevels": ["medium", "high"],
            "prohibitedMutations": [],
        },
        "metadata": {"createdBy": "operating-graph", "createdAt": TIMESTAMP},
    }


def graph(data: dict[str, object] | None = None) -> Graph:
    return Graph.from_dict(data or valid_graph_data())


def codes(violations: object) -> list[str]:
    return [violation.code for violation in violations]


class GraphInvariantTests(unittest.TestCase):
    def test_valid_graph_satisfies_all_structural_invariants(self) -> None:
        self.assertEqual(validate_graph_invariants(graph()), ())

    def test_01_node_and_edge_ids_are_unique(self) -> None:
        data = valid_graph_data()
        data["nodes"].append(deepcopy(data["nodes"][2]))
        data["edges"].append(deepcopy(data["edges"][0]))

        self.assertIn("OGI-01", codes(validate_graph_invariants(graph(data))))

    def test_02_ids_use_lowercase_letters_digits_and_hyphens(self) -> None:
        data = valid_graph_data()
        data["nodes"][2]["id"] = "Bad_ID"

        self.assertIn("OGI-02", codes(validate_graph_invariants(graph(data))))

    def test_03_every_edge_endpoint_exists(self) -> None:
        data = valid_graph_data()
        data["edges"][0]["target"] = "missing-node"

        self.assertIn("OGI-03", codes(validate_graph_invariants(graph(data))))

        data = valid_graph_data()
        data["edges"][0]["activation"]["nodeStates"] = [{"nodeId": "missing-node", "status": "succeeded"}]
        self.assertIn("OGI-03", codes(validate_graph_invariants(graph(data))))

    def test_04_exactly_one_enabled_authority_exists(self) -> None:
        data = valid_graph_data()
        data["nodes"][0]["enabled"] = False

        self.assertIn("OGI-04", codes(validate_graph_invariants(graph(data))))

    def test_05_exactly_one_enabled_controller_exists(self) -> None:
        data = valid_graph_data()
        data["nodes"][1]["enabled"] = False

        self.assertIn("OGI-05", codes(validate_graph_invariants(graph(data))))

    def test_06_goal_authority_id_points_to_the_enabled_authority(self) -> None:
        data = valid_graph_data()
        data["goal"]["authorityNodeId"] = "controller"

        self.assertIn("OGI-06", codes(validate_graph_invariants(graph(data))))

    def test_07_immutable_boundaries_match_the_original_graph(self) -> None:
        original = graph()
        mutations = (
            ("goal", lambda data: data["goal"].update(statement="Different goal.")),
            ("deliverables", lambda data: data["goal"]["deliverables"][0].update(description="Changed.")),
            ("criteria", lambda data: data["goal"].update(completionCriteria=["Weaker criterion."])),
            ("authority", lambda data: data["goal"].update(authorityNodeId="controller")),
            ("permissions", lambda data: data["nodes"][2].update(capabilities=["network-write"])),
            ("approvals", lambda data: data["edges"][4].update(required=False)),
            ("hard-limits", lambda data: data["limits"].update(maxNodeRuns=21)),
            ("rewrite-approvals", lambda data: data["rewritePolicy"].update(approvalRiskLevels=["high"])),
            ("prohibited-mutations", lambda data: data["rewritePolicy"].update(prohibitedMutations=["goal.statement"])),
        )
        for label, mutate in mutations:
            data = valid_graph_data()
            mutate(data)
            with self.subTest(label=label):
                self.assertIn("OGI-07", codes(validate_rewritten_graph(graph(data), original_graph=original)))

    def test_07_permissions_are_compared_per_node_not_as_a_union(self) -> None:
        original_data = valid_graph_data()
        original_data["nodes"][2]["capabilities"] = ["research"]
        original_data["nodes"][3]["capabilities"] = ["evaluation"]
        original = graph(original_data)
        changed = deepcopy(original_data)
        changed["nodes"][2]["capabilities"] = ["evaluation"]
        changed["nodes"][3]["capabilities"] = ["research"]

        self.assertIn("OGI-07", codes(validate_rewritten_graph(graph(changed), original_graph=original)))

    def test_08_every_enabled_node_is_reachable_from_authority(self) -> None:
        data = valid_graph_data()
        data["nodes"].append(node("orphan", "worker"))

        self.assertIn("OGI-08", codes(validate_graph_invariants(graph(data))))

    def test_09_every_required_deliverable_has_an_enabled_producer(self) -> None:
        data = valid_graph_data()
        data["goal"]["deliverables"][0]["artifactType"] = "missing-report"

        self.assertIn("OGI-09", codes(validate_graph_invariants(graph(data))))

    def test_10_every_required_deliverable_has_an_independent_evaluator_path(self) -> None:
        data = valid_graph_data()
        data["edges"][2]["enabled"] = False

        self.assertIn("OGI-10", codes(validate_graph_invariants(graph(data))))

    def test_10_evaluator_requires_explicit_matching_verify_edge(self) -> None:
        data = valid_graph_data()
        data["edges"][2]["artifactTypes"] = []
        self.assertIn("OGI-10", codes(validate_graph_invariants(graph(data))))

        data = valid_graph_data()
        data["nodes"].append(node("relay", "worker"))
        data["edges"][2]["target"] = "relay"
        data["edges"].append(edge("relay-to-evaluator", "relay", "evaluator", "write", artifact_types=["report"]))
        self.assertIn("OGI-10", codes(validate_graph_invariants(graph(data))))

    def test_10_independent_evaluator_may_output_the_same_artifact_type(self) -> None:
        data = valid_graph_data()
        data["nodes"][3]["outputs"] = [{"artifactType": "report", "required": True}]

        self.assertNotIn("OGI-10", codes(validate_graph_invariants(graph(data))))

    def test_11_node_cannot_evaluate_or_approve_its_own_output(self) -> None:
        for kind in ("verify", "approve"):
            data = valid_graph_data()
            data["edges"].append(edge(f"producer-self-{kind}", "producer", "producer", kind))
            with self.subTest(kind=kind):
                self.assertIn("OGI-11", codes(validate_graph_invariants(graph(data))))

    def test_11_indirect_self_evaluation_and_approval_paths_are_rejected(self) -> None:
        for kind in ("verify", "approve"):
            data = valid_graph_data()
            data["nodes"].append(node("relay", "worker"))
            data["edges"].append(edge("producer-to-relay", "producer", "relay", "write", artifact_types=["report"]))
            data["edges"].append(edge(f"relay-to-producer-{kind}", "relay", "producer", kind, artifact_types=["report"]))
            with self.subTest(kind=kind):
                self.assertIn("OGI-11", codes(validate_graph_invariants(graph(data))))

    def test_11_next_epoch_feedback_after_independent_verification_is_not_self_evaluation(self) -> None:
        data = valid_graph_data()
        data["edges"].append(
            edge(
                "evaluator-feedback",
                "evaluator",
                "producer",
                "learn",
                temporal="next_epoch",
            )
        )

        self.assertEqual(validate_graph_invariants(graph(data)), ())

    def test_12_external_side_effect_node_has_required_authority_approval_predecessor(self) -> None:
        data = valid_graph_data()
        data["edges"][4]["enabled"] = False

        self.assertIn("OGI-12", codes(validate_graph_invariants(graph(data))))

    def test_12_external_classification_covers_tools_publish_edges_and_unknown_capabilities(self) -> None:
        cases = (
            ("tool", lambda data: data["nodes"][2]["execution"].update(mode="tool")),
            ("publish", lambda data: data["edges"].append(edge("producer-publishes", "producer", "publisher", "publish"))),
            ("unknown-capability", lambda data: data["nodes"][2].update(capabilities=["custom-action"])),
        )
        for label, mutate in cases:
            data = valid_graph_data()
            mutate(data)
            with self.subTest(label=label):
                violations = validate_graph_invariants(graph(data))
                self.assertTrue(any(item.code == "OGI-12" and item.location == "nodes.producer" for item in violations))

    def test_13_enabled_same_epoch_dependencies_are_acyclic(self) -> None:
        data = valid_graph_data()
        data["edges"].append(edge("evaluator-to-producer", "evaluator", "producer", "learn"))

        self.assertIn("OGI-13", codes(validate_graph_invariants(graph(data))))

    def test_14_every_enabled_cycle_contains_a_next_epoch_edge(self) -> None:
        data = valid_graph_data()
        data["edges"].append(edge("evaluator-to-producer", "evaluator", "producer", "learn"))

        self.assertIn("OGI-14", codes(validate_graph_invariants(graph(data))))

    def test_feedback_cycle_with_next_epoch_edge_and_positive_limit_is_valid(self) -> None:
        data = valid_graph_data()
        data["edges"].append(
            edge("evaluator-to-producer", "evaluator", "producer", "learn", temporal="next_epoch")
        )

        temporal_codes = codes(validate_graph_invariants(graph(data)))
        self.assertNotIn("OGI-13", temporal_codes)
        self.assertNotIn("OGI-14", temporal_codes)
        self.assertNotIn("OGI-15", temporal_codes)

    def test_15_next_epoch_edges_require_a_finite_positive_max_epochs(self) -> None:
        data = valid_graph_data()
        data["edges"][2]["temporal"] = "next_epoch"
        data["limits"]["maxEpochs"] = 0

        self.assertIn("OGI-15", codes(validate_graph_invariants(graph(data))))

    def test_16_runtime_limits_are_positive_integers(self) -> None:
        for limit in (
            "maxConcurrentWorkers", "maxNodeRuns", "maxGraphVersions", "maxEpochs",
            "maxAutoRewrites", "defaultMaxAttempts",
        ):
            data = valid_graph_data()
            data["limits"][limit] = 0
            with self.subTest(limit=limit):
                self.assertIn("OGI-16", codes(validate_graph_invariants(graph(data))))

        data = valid_graph_data()
        data["nodes"][2]["budget"]["maxAttempts"] = 0
        data["nodes"][2]["budget"]["workUnits"] = 0
        data["nodes"][2]["localLoop"]["maxIterations"] = 0
        self.assertEqual(codes(validate_graph_invariants(graph(data))).count("OGI-16"), 3)

        runtime = RuntimeState.from_dict({
            "runId": "run-1", "graphId": "verified-report", "graphVersion": 1, "epoch": 4,
            "status": "running", "nodeStates": {"producer": {"nodeId": "producer", "status": "running", "attempts": 3}},
            "totalNodeRuns": 21, "autoRewritesApplied": 3,
        })
        runtime_codes = codes(
            validate_runtime_limits(
                graph(), runtime, current_concurrency=3, graph_version_count=11
            )
        )
        self.assertIn("OGI-15", runtime_codes)
        self.assertEqual(runtime_codes.count("OGI-16"), 5)

    def test_17_required_artifact_types_have_enabled_producers(self) -> None:
        data = valid_graph_data()
        data["nodes"][3]["inputs"].append({"artifactType": "rubric", "required": True})

        self.assertIn("OGI-17", codes(validate_graph_invariants(graph(data))))

    def test_09_and_17_require_enabled_required_outputs(self) -> None:
        data = valid_graph_data()
        data["nodes"][2]["outputs"][0]["required"] = False

        invariant_codes = codes(validate_graph_invariants(graph(data)))
        self.assertIn("OGI-09", invariant_codes)
        self.assertIn("OGI-17", invariant_codes)

    def test_17_required_edge_artifact_must_be_produced_by_its_source(self) -> None:
        data = valid_graph_data()
        data["edges"][2]["source"] = "controller"

        self.assertIn("OGI-17", codes(validate_graph_invariants(graph(data))))

    def test_18_disabled_nodes_cannot_satisfy_dependencies(self) -> None:
        data = valid_graph_data()
        data["nodes"][2]["enabled"] = False

        self.assertIn("OGI-18", codes(validate_graph_invariants(graph(data))))

        runtime = RuntimeState.from_dict({
            "runId": "run-1", "graphId": "verified-report", "graphVersion": 1, "epoch": 1,
            "status": "running", "nodeStates": {"producer": {"nodeId": "producer", "status": "succeeded"}},
        })
        self.assertNotIn(
            "OGI-18",
            codes(validate_runtime_dependencies(graph(data), runtime, satisfactions=[])),
        )
        self.assertIn(
            "OGI-18",
            codes(
                validate_runtime_dependencies(
                    graph(data), runtime, satisfactions=[("evaluator", "producer")]
                )
            ),
        )

    def test_19_free_form_condition_fields_are_rejected(self) -> None:
        data = valid_graph_data()
        data["nodes"][2]["condition"] = "artifact_ready and eval(payload)"

        self.assertIn("OGI-19", codes(parse_and_validate_graph(data).violations))

    def test_19_human_readable_stop_criteria_are_not_treated_as_executable_conditions(self) -> None:
        data = valid_graph_data()
        data["nodes"][2]["localLoop"]["stopCondition"] = "Explain why eval(payload) is forbidden."

        self.assertNotIn("OGI-19", codes(validate_graph_invariants(graph(data))))

    def test_19_executable_stop_conditions_are_rejected_syntactically(self) -> None:
        conditions = (
            "check_ready()",
            "ready = check_ready()",
            "checkStatus(payload)",
            "ready && publish()",
            "$(publish report)",
        )
        for condition in conditions:
            data = valid_graph_data()
            data["nodes"][2]["localLoop"]["stopCondition"] = condition
            with self.subTest(condition=condition):
                self.assertIn("OGI-19", codes(validate_graph_invariants(graph(data))))

    def test_19_positive_grammar_accepts_clear_human_sentences(self) -> None:
        for condition in (
            "All checks pass; evidence exists.",
            "The `report` exists",
            "Open the report when approval is granted.",
            "Find the final report in the artifact registry.",
            "Make sure the report exists.",
        ):
            data = valid_graph_data()
            data["nodes"][2]["localLoop"]["stopCondition"] = condition
            with self.subTest(condition=condition):
                self.assertNotIn("OGI-19", codes(validate_graph_invariants(graph(data))))

    def test_19_positive_grammar_accepts_only_explicit_simple_status_labels(self) -> None:
        for condition in (
            "approved",
            "complete",
            "completed",
            "ready",
            "done",
            "success",
            "succeeded",
            "verified",
            "passed",
        ):
            data = valid_graph_data()
            data["nodes"][2]["localLoop"]["stopCondition"] = condition
            with self.subTest(condition=condition):
                self.assertNotIn("OGI-19", codes(validate_graph_invariants(graph(data))))

    def test_19_command_shaped_or_ambiguous_text_is_rejected_by_default(self) -> None:
        for condition in (
            "date",
            "id",
            "head report.md",
            "sleep 1",
            "echo completed",
            "curl https://example.invalid",
            'sh -c "touch /tmp/x"',
            "mybinary arg",
            "All checks pass; mybinary arg.",
        ):
            data = valid_graph_data()
            data["nodes"][2]["localLoop"]["stopCondition"] = condition
            with self.subTest(condition=condition):
                self.assertIn("OGI-19", codes(validate_graph_invariants(graph(data))))

    def test_20_paths_cannot_escape_the_run_directory(self) -> None:
        artifact = Artifact.from_dict({
            "artifactId": "artifact-1", "runId": "run-1", "nodeId": "producer", "graphVersion": 1,
            "type": "report", "path": "../outside.md", "mediaType": "text/markdown", "sha256": "abc",
            "createdAt": TIMESTAMP, "supersedes": None, "evidence": [],
        })
        with tempfile.TemporaryDirectory() as run_directory:
            self.assertIn("OGI-20", codes(validate_artifact_path(artifact, Path(run_directory))))

        wrongly_owned = Artifact.from_dict({
            **artifact.to_dict(),
            "path": "artifacts/evaluator/artifact-1.md",
        })
        with tempfile.TemporaryDirectory() as run_directory:
            self.assertIn("OGI-20", codes(validate_artifact_path(wrongly_owned, Path(run_directory))))

    def test_20_malformed_paths_return_violations_instead_of_raising(self) -> None:
        for malformed in ("artifacts/producer/bad\x00name.md", "artifacts/producer/bad\nname.md"):
            artifact = Artifact.from_dict({
                "artifactId": "artifact-1", "runId": "run-1", "nodeId": "producer", "graphVersion": 1,
                "type": "report", "path": malformed, "mediaType": "text/markdown", "sha256": "abc",
                "createdAt": TIMESTAMP, "supersedes": None, "evidence": [],
            })
            with self.subTest(malformed=repr(malformed)), tempfile.TemporaryDirectory() as run_directory:
                try:
                    violations = validate_artifact_path(artifact, Path(run_directory))
                except (OSError, ValueError) as error:
                    self.fail(f"path validator raised {type(error).__name__}: {error}")
                self.assertIn("OGI-20", codes(violations))

    def test_21_applied_rewrite_references_a_valid_base_and_rollback_version(self) -> None:
        proposal = RewriteProposal.from_dict({
            "proposalId": "rewrite-1", "runId": "run-1", "baseGraphVersion": 3, "trigger": "failure",
            "evidenceEventIds": [], "riskLevel": "low", "reason": "Retry.", "predictedEffect": "Recovery.",
            "operations": [], "approvalRequired": False, "rollbackVersion": 4,
        })

        self.assertEqual(codes(validate_applied_rewrite(proposal, available_versions={1, 2})), ["OGI-21", "OGI-21"])

    def test_22_graph_versions_are_sequential_and_immutable(self) -> None:
        versions = {1: graph(), 3: graph()}
        canonical = json.dumps(versions[1].to_dict(), sort_keys=True, separators=(",", ":"))
        wrong_digest = hashlib.sha256((canonical + "changed").encode()).hexdigest()

        violations = validate_graph_versions(versions, immutable_hashes={1: wrong_digest})

        self.assertEqual(codes(violations), ["OGI-22", "OGI-22", "OGI-22"])

    def test_22_requires_complete_trusted_digest_coverage(self) -> None:
        versions = {1: graph(), 2: graph()}
        canonical = json.dumps(versions[1].to_dict(), sort_keys=True, separators=(",", ":"))
        digest = hashlib.sha256(canonical.encode()).hexdigest()

        self.assertIn("OGI-22", codes(validate_graph_versions(versions)))
        self.assertIn("OGI-22", codes(validate_graph_versions(versions, immutable_hashes={})))
        partial = validate_graph_versions(versions, immutable_hashes={1: digest})
        self.assertTrue(any(item.code == "OGI-22" and "version 2" in item.message for item in partial))
        self.assertEqual(validate_graph_versions(versions, immutable_hashes={1: digest, 2: digest}), ())

    def test_all_violations_are_returned_once_in_deterministic_order(self) -> None:
        data = valid_graph_data()
        data["nodes"][0]["enabled"] = False
        data["nodes"][1]["enabled"] = False
        data["nodes"][2]["id"] = "Bad_ID"
        data["edges"][0]["target"] = "missing-node"
        data["limits"]["maxNodeRuns"] = 0
        invalid = graph(data)

        first = validate_graph_invariants(invalid)
        second = validate_graph_invariants(invalid)

        self.assertEqual(first, second)
        self.assertGreater(len(first), 4)
        self.assertEqual(
            [(item.invariant, item.location, item.message) for item in first],
            sorted((item.invariant, item.location, item.message) for item in first),
        )


if __name__ == "__main__":
    unittest.main()
