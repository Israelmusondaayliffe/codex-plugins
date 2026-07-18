"""Validation contracts for Operating Graph's serializable model layer."""

from __future__ import annotations

import unittest

import scripts.graph_engine.validation as graph_validation

from scripts.graph_engine.constants import NodeKind, NodeStatus, RewriteOperationKind, VerificationStatus
from scripts.graph_engine.models import (
    Activation,
    Approval,
    Artifact,
    Deliverable,
    Edge,
    Event,
    Graph,
    Goal,
    Node,
    NodeRuntimeState,
    RewriteOperation,
    RewriteProposal,
    RuntimeState,
    VerificationResult,
)
from scripts.graph_engine.validation import (
    GraphValidationError,
    parse_and_validate_graph,
    require_valid_graph,
    validate_structure,
)


TIMESTAMP = "2026-07-18T12:00:00Z"


def valid_node() -> dict[str, object]:
    return {
        "id": "researcher",
        "kind": "worker",
        "label": "Researcher",
        "purpose": "Gather verified information.",
        "enabled": True,
        "critical": True,
        "priority": 70,
        "execution": {"mode": "subagent", "skill": None, "modelHint": None},
        "capabilities": ["research", "artifact-write"],
        "inputs": [{"artifactType": "research-brief", "required": True}],
        "outputs": [{"artifactType": "verified-research", "required": True}],
        "successCriteria": ["Evidence is registered."],
        "budget": {"maxAttempts": 2, "workUnits": 5},
        "localLoop": {
            "enabled": True,
            "maxIterations": 3,
            "sequence": ["attempt", "inspect", "evaluate", "correct"],
            "stopCondition": "Criteria are satisfied.",
        },
    }


def valid_edge() -> dict[str, object]:
    return {
        "id": "research-to-builder",
        "source": "researcher",
        "target": "builder",
        "kind": "write",
        "enabled": True,
        "required": True,
        "temporal": "same_epoch",
        "artifactTypes": ["verified-research"],
        "activation": {
            "mode": "all",
            "nodeStates": [{"nodeId": "researcher", "status": "succeeded"}],
            "artifacts": ["verified-research"],
            "approvals": [],
        },
    }


def valid_graph() -> dict[str, object]:
    return {
        "schemaVersion": "1.0",
        "graphId": "research-build-review",
        "name": "Research Build Review",
        "goal": {
            "statement": "Produce a verified deliverable.",
            "deliverables": [
                {
                    "id": "final-report",
                    "artifactType": "report",
                    "description": "A verified final report.",
                }
            ],
            "completionCriteria": ["The final report exists."],
            "authorityNodeId": "human-authority",
        },
        "limits": {
            "maxConcurrentWorkers": 3,
            "maxNodeRuns": 30,
            "maxGraphVersions": 20,
            "maxEpochs": 5,
            "maxAutoRewrites": 5,
            "defaultMaxAttempts": 2,
        },
        "nodes": [valid_node()],
        "edges": [valid_edge()],
        "rewritePolicy": {
            "automaticRiskLevels": ["low"],
            "approvalRiskLevels": ["medium", "high"],
            "prohibitedMutations": [],
        },
        "metadata": {"createdBy": "operating-graph", "createdAt": TIMESTAMP},
    }


def valid_event() -> dict[str, object]:
    return {
        "eventId": "evt-000001",
        "sequence": 1,
        "timestamp": TIMESTAMP,
        "runId": "run-001",
        "graphVersion": 1,
        "actorNodeId": "controller",
        "type": "node.started",
        "payload": {"nested": {"items": ["original"]}},
        "previousHash": None,
        "eventHash": "abc",
    }


class ModelParsingTests(unittest.TestCase):
    def test_graph_parses_the_canonical_nested_contract(self) -> None:
        graph = Graph.from_dict(valid_graph())

        self.assertEqual(graph.graph_id, "research-build-review")
        self.assertEqual(graph.goal.deliverables[0].artifact_type, "report")
        self.assertEqual(graph.nodes[0].kind, NodeKind.WORKER)
        self.assertEqual(graph.edges[0].activation.node_states[0].status, NodeStatus.SUCCEEDED)

    def test_graph_serializes_back_to_the_canonical_contract(self) -> None:
        self.assertEqual(Graph.from_dict(valid_graph()).to_dict(), valid_graph())

    def test_graph_rejects_a_missing_required_field(self) -> None:
        payload = valid_graph()
        del payload["graphId"]

        with self.assertRaisesRegex(ValueError, r"Graph\.graphId: missing required field"):
            Graph.from_dict(payload)

    def test_node_rejects_a_non_object_execution(self) -> None:
        payload = valid_node()
        payload["execution"] = "subagent"

        with self.assertRaisesRegex(ValueError, r"Node\.execution: expected object"):
            Node.from_dict(payload)

    def test_edge_rejects_an_unknown_enum_value(self) -> None:
        payload = valid_edge()
        payload["temporal"] = "later"

        with self.assertRaisesRegex(ValueError, r"Edge\.temporal: invalid Temporal value 'later'"):
            Edge.from_dict(payload)

    def test_runtime_state_parses_node_runtime_state(self) -> None:
        runtime = RuntimeState.from_dict(
            {
                "runId": "run-001",
                "graphId": "research-build-review",
                "graphVersion": 1,
                "status": "running",
                "epoch": 1,
                "nodeStates": {
                    "researcher": {
                        "nodeId": "researcher",
                        "status": "running",
                        "attempts": 1,
                        "lastError": None,
                        "blocker": None,
                        "completedEpoch": None,
                        "outputArtifactIds": [],
                    }
                },
                "totalNodeRuns": 1,
                "autoRewritesApplied": 0,
                "budgetThresholdsEmitted": [],
            }
        )

        self.assertEqual(runtime.node_states["researcher"].status, NodeStatus.RUNNING)

    def test_runtime_and_approval_parsers_use_declared_defaults(self) -> None:
        node_state = NodeRuntimeState.from_dict({"nodeId": "researcher", "status": "ready"})
        runtime = RuntimeState.from_dict(
            {
                "runId": "run-001",
                "graphId": "research-build-review",
                "graphVersion": 1,
                "epoch": 1,
                "status": "running",
                "nodeStates": {"researcher": {"nodeId": "researcher", "status": "ready"}},
            }
        )
        approval = Approval.from_dict(
            {
                "approvalId": "approval-0001",
                "runId": "run-001",
                "subjectType": "rewrite",
                "subjectId": "rewrite-0001",
                "requestedBy": "controller",
                "requiredFrom": "human-authority",
                "status": "pending",
                "requestedAt": TIMESTAMP,
            }
        )

        self.assertEqual(node_state.attempts, 0)
        self.assertEqual(runtime.total_node_runs, 0)
        self.assertEqual(runtime.auto_rewrites_applied, 0)
        self.assertEqual(approval.resolved_at, None)

    def test_event_rejects_a_boolean_for_an_integer(self) -> None:
        payload = valid_event()
        payload["sequence"] = True

        with self.assertRaisesRegex(ValueError, r"Event\.sequence: expected integer"):
            Event.from_dict(payload)

    def test_event_hash_uses_an_owned_canonical_snapshot(self) -> None:
        payload = valid_event()
        event = Event.from_dict(payload)
        expected_hash = event.calculated_hash()
        expected_json = event.canonical_json()

        payload["payload"]["nested"]["items"].append("caller mutation")
        event.payload["nested"]["items"].append("exposed mutation")

        self.assertEqual(event.calculated_hash(), expected_hash)
        self.assertEqual(event.canonical_json(), expected_json)
        self.assertEqual(event.to_dict()["payload"], {"nested": {"items": ["original"]}})

    def test_event_payload_rejects_non_json_data_recursively(self) -> None:
        cases = (
            ({1: "not a string key"}, r"Event\.payload: expected string keys"),
            ({"number": float("nan")}, r"Event\.payload\.number: expected finite number"),
            ({"number": float("inf")}, r"Event\.payload\.number: expected finite number"),
            ({"unsupported": {"value"}}, r"Event\.payload\.unsupported: expected JSON value"),
        )

        for invalid_payload, message in cases:
            payload = valid_event()
            payload["payload"] = invalid_payload
            with self.subTest(invalid_payload=invalid_payload), self.assertRaisesRegex(ValueError, message):
                Event.from_dict(payload)

    def test_all_timestamp_fields_require_canonical_utc(self) -> None:
        artifact = {
            "artifactId": "art-000001", "runId": "run-001", "nodeId": "researcher", "graphVersion": 1,
            "type": "verified-research", "path": "artifacts/researcher/art-000001.md", "mediaType": "text/markdown",
            "sha256": "abc", "createdAt": "2026-07-18T12:00:00", "supersedes": None, "evidence": [],
        }
        approval = {
            "approvalId": "approval-0001", "runId": "run-001", "subjectType": "artifact", "subjectId": "art-000001",
            "requestedBy": "researcher", "requiredFrom": "human-authority", "status": "pending",
            "requestedAt": "2026-07-18", "resolvedAt": None, "resolvedBy": None, "reason": None,
        }
        verification = {
            "status": "pass", "checkedAt": "2026-07-18T08:00:00-04:00", "criteria": [], "issues": [],
            "evidenceArtifactIds": [],
        }
        event = valid_event()
        event["timestamp"] = "2026-07-18T12:00:00+00:00"
        graph = valid_graph()
        graph["metadata"] = {"createdBy": "operating-graph", "createdAt": "2026-07-18"}

        cases = (
            (Graph, graph, r"Graph\.metadata\.createdAt: expected canonical UTC timestamp"),
            (Event, event, r"Event\.timestamp: expected canonical UTC timestamp"),
            (Artifact, artifact, r"Artifact\.createdAt: expected canonical UTC timestamp"),
            (Approval, approval, r"Approval\.requestedAt: expected canonical UTC timestamp"),
            (VerificationResult, verification, r"VerificationResult\.checkedAt: expected canonical UTC timestamp"),
        )
        for model, payload, message in cases:
            with self.subTest(model=model.__name__), self.assertRaisesRegex(ValueError, message):
                model.from_dict(payload)


    def test_open_json_model_fields_reject_invalid_nested_data(self) -> None:
        cases = (
            (RewriteOperation, {"kind": "set_priority", "params": {"bad": float("nan")}}, r"RewriteOperation\.params\.bad: expected finite number"),
            (VerificationResult, {"status": "pass", "checkedAt": TIMESTAMP, "criteria": [{"bad": {1: "key"}}], "issues": [], "evidenceArtifactIds": []}, r"VerificationResult\.criteria\[0\]\.bad: expected string keys"),
        )

        for model, payload, message in cases:
            with self.subTest(model=model.__name__), self.assertRaisesRegex(ValueError, message):
                model.from_dict(payload)

    def test_additive_unknown_fields_are_ignored(self) -> None:
        graph_payload = valid_graph()
        graph_payload["futureField"] = {"schema": 2}
        graph_payload["nodes"][0]["futureNodeField"] = "ignored"
        event_payload = valid_event()
        event_payload["futureField"] = True

        self.assertNotIn("futureField", Graph.from_dict(graph_payload).to_dict())
        self.assertNotIn("futureField", Event.from_dict(event_payload).to_dict())

    def test_mutable_dataclass_defaults_are_isolated(self) -> None:
        first_node = NodeRuntimeState("one", NodeStatus.PENDING)
        second_node = NodeRuntimeState("two", NodeStatus.PENDING)
        first_operation = RewriteOperation(RewriteOperationKind.SET_PRIORITY)
        second_operation = RewriteOperation(RewriteOperationKind.SET_PRIORITY)

        first_node.output_artifact_ids.append("art-1")
        first_operation.params["priority"] = 80

        self.assertEqual(second_node.output_artifact_ids, [])
        self.assertEqual(second_operation.params, {})

    def test_requested_models_reject_wrong_scalar_container_nested_and_enum_types(self) -> None:
        activation = {
            "mode": "all", "nodeStates": [{"nodeId": "researcher", "status": "succeeded"}],
            "artifacts": [], "approvals": [],
        }
        runtime = {
            "runId": "run-001", "graphId": "graph", "graphVersion": 1, "epoch": 1, "status": "running",
            "nodeStates": {},
        }
        artifact = {
            "artifactId": "art-000001", "runId": "run-001", "nodeId": "researcher", "graphVersion": 1,
            "type": "report", "path": "artifacts/researcher/art-000001.md", "mediaType": "text/markdown",
            "sha256": "abc", "createdAt": TIMESTAMP, "supersedes": None, "evidence": [],
        }
        approval = {
            "approvalId": "approval-0001", "runId": "run-001", "subjectType": "artifact", "subjectId": "art-000001",
            "requestedBy": "researcher", "requiredFrom": "human-authority", "status": "pending", "requestedAt": TIMESTAMP,
        }
        proposal = {
            "proposalId": "rewrite-0001", "runId": "run-001", "baseGraphVersion": 1, "trigger": "failure",
            "evidenceEventIds": [], "riskLevel": "low", "reason": "reason", "predictedEffect": "effect",
            "operations": [], "approvalRequired": False, "rollbackVersion": 1,
        }
        cases = (
            (Deliverable, {"id": "report", "artifactType": "report", "description": True}, r"Deliverable\.description: expected string"),
            (Goal, {"statement": "goal", "deliverables": {}, "completionCriteria": [], "authorityNodeId": "authority"}, r"Goal\.deliverables: expected array"),
            (Activation, {**activation, "nodeStates": ["researcher"]}, r"NodeStateRequirement: expected object"),
            (Node, {**valid_node(), "kind": "unknown"}, r"Node\.kind: invalid NodeKind value 'unknown'"),
            (Edge, {**valid_edge(), "artifactTypes": {}}, r"Edge\.artifactTypes: expected array"),
            (NodeRuntimeState, {"nodeId": "node", "status": "unknown"}, r"NodeRuntimeState\.status: invalid NodeStatus value 'unknown'"),
            (RuntimeState, {**runtime, "nodeStates": []}, r"RuntimeState\.nodeStates: expected object"),
            (Event, {**valid_event(), "type": []}, r"Event\.type: expected string"),
            (Artifact, {**artifact, "evidence": {}}, r"Artifact\.evidence: expected array"),
            (Approval, {**approval, "subjectType": "unknown"}, r"Approval\.subjectType: invalid ApprovalSubjectType value 'unknown'"),
            (RewriteOperation, {"kind": "unknown", "params": {}}, r"RewriteOperation\.kind: invalid RewriteOperationKind value 'unknown'"),
            (RewriteProposal, {**proposal, "operations": {}}, r"RewriteProposal\.operations: expected array"),
            (VerificationResult, {"status": "unknown", "checkedAt": TIMESTAMP, "criteria": [], "issues": [], "evidenceArtifactIds": []}, r"VerificationResult\.status: invalid VerificationStatus value 'unknown'"),
        )

        for model, payload, message in cases:
            with self.subTest(model=model.__name__), self.assertRaisesRegex(ValueError, message):
                model.from_dict(payload)

    def test_artifact_approval_rewrite_and_verification_parse(self) -> None:
        artifact = Artifact.from_dict(
            {
                "artifactId": "art-000001",
                "runId": "run-001",
                "nodeId": "researcher",
                "graphVersion": 1,
                "type": "verified-research",
                "path": "artifacts/researcher/art-000001.md",
                "mediaType": "text/markdown",
                "sha256": "abc",
                "createdAt": TIMESTAMP,
                "supersedes": None,
                "evidence": [{"source": "brief.md", "claim": "Supported claim.", "confidence": "high"}],
            }
        )
        approval = Approval.from_dict(
            {
                "approvalId": "approval-0001",
                "runId": "run-001",
                "requestedBy": "researcher",
                "requiredFrom": "human-authority",
                "subjectType": "artifact",
                "subjectId": "art-000001",
                "status": "granted",
                "requestedAt": TIMESTAMP,
                "resolvedAt": TIMESTAMP,
                "resolvedBy": "human-authority",
                "reason": "Evidence reviewed.",
            }
        )
        operation = RewriteOperation.from_dict(
            {"kind": "set_priority", "params": {"nodeId": "researcher", "priority": 80}}
        )
        proposal = RewriteProposal.from_dict(
            {
                "proposalId": "rewrite-0001",
                "runId": "run-001",
                "baseGraphVersion": 1,
                "trigger": "repeated-node-failure",
                "evidenceEventIds": ["evt-000021"],
                "riskLevel": "medium",
                "reason": "The node failed twice.",
                "predictedEffect": "Introduce an evaluator.",
                "operations": [{"kind": "set_priority", "params": {"nodeId": "researcher", "priority": 80}}],
                "approvalRequired": True,
                "rollbackVersion": 1,
            }
        )
        verification = VerificationResult.from_dict(
            {
                "status": "pass",
                "criteria": [{"criterion": "The final report exists.", "passed": True}],
                "evidenceArtifactIds": ["art-000001"],
                "issues": [],
                "checkedAt": TIMESTAMP,
            }
        )

        self.assertEqual(artifact.evidence[0].confidence.value, "high")
        self.assertEqual(approval.status.value, "granted")
        self.assertEqual(operation.kind.value, "set_priority")
        self.assertEqual(proposal.operations[0].params["nodeId"], "researcher")
        self.assertEqual(verification.status, VerificationStatus.PASS)

    def test_runtime_artifact_approval_rewrite_and_verification_reject_bad_types(self) -> None:
        invalid_cases = (
            (NodeRuntimeState, {"nodeId": "n", "status": "ready", "attempts": "1", "lastError": None, "blocker": None, "completedEpoch": None, "outputArtifactIds": []}, r"NodeRuntimeState\.attempts: expected integer"),
            (Artifact, {"artifactId": "a"}, r"Artifact\.runId: missing required field"),
            (Approval, {"approvalId": "a"}, r"Approval\.runId: missing required field"),
            (RewriteOperation, {"kind": "set_priority", "params": []}, r"RewriteOperation\.params: expected object"),
            (VerificationResult, {"status": "pass"}, r"VerificationResult\.checkedAt: missing required field"),
        )

        for model, payload, message in invalid_cases:
            with self.subTest(model=model.__name__), self.assertRaisesRegex(ValueError, message):
                model.from_dict(payload)


class StructuralValidationTests(unittest.TestCase):
    def test_structural_validation_returns_all_independently_detectable_errors(self) -> None:
        payload = valid_graph()
        del payload["graphId"]
        del payload["name"]
        del payload["goal"]["statement"]
        del payload["goal"]["completionCriteria"]

        violations = validate_structure(payload)

        messages = [violation.message for violation in violations]
        self.assertIn("Graph.graphId: missing required field", messages)
        self.assertIn("Graph.name: missing required field", messages)
        self.assertIn("Goal.statement: missing required field", messages)
        self.assertIn("Goal.completionCriteria: missing required field", messages)

    def test_structural_validation_collects_independent_closed_value_errors(self) -> None:
        payload = valid_graph()
        payload["nodes"][0]["kind"] = "unknown-node-kind"
        payload["edges"][0]["temporal"] = "later"
        payload["metadata"]["createdAt"] = "not-a-timestamp"

        messages = [violation.message for violation in validate_structure(payload)]

        self.assertIn("Node.kind: invalid NodeKind value 'unknown-node-kind'", messages)
        self.assertIn("Edge.temporal: invalid Temporal value 'later'", messages)
        self.assertIn("Graph.metadata.createdAt: expected canonical UTC timestamp", messages)

    def test_structural_validation_rejects_an_unsupported_schema_version(self) -> None:
        payload = valid_graph()
        payload["schemaVersion"] = "2.0"

        violations = validate_structure(payload)

        self.assertEqual(len(violations), 1)
        self.assertEqual(violations[0].code, "STRUCTURE")
        self.assertIn("unsupported schemaVersion", violations[0].message)

    def test_parse_and_validate_graph_keeps_the_parsed_graph_and_invariant_failures(self) -> None:
        payload = valid_graph()

        result = parse_and_validate_graph(payload)

        self.assertIsNotNone(result.graph)
        self.assertFalse(result.valid)
        self.assertIn("OGI-04", [violation.code for violation in result.violations])

    def test_unsupported_schema_does_not_suppress_invariant_collection(self) -> None:
        payload = valid_graph()
        payload["schemaVersion"] = "2.0"

        result = parse_and_validate_graph(payload)

        violation_codes = [violation.code for violation in result.violations]
        self.assertIn("STRUCTURE", violation_codes)
        self.assertIn("OGI-04", violation_codes)
        self.assertIn("OGI-05", violation_codes)

    def test_malformed_graph_still_returns_independent_raw_condition_violation(self) -> None:
        payload = valid_graph()
        del payload["graphId"]
        payload["nodes"][0]["condition"] = "run_code()"

        result = parse_and_validate_graph(payload)

        self.assertIsNone(result.graph)
        self.assertIn("STRUCTURE", [item.code for item in result.violations])
        self.assertIn("OGI-19", [item.code for item in result.violations])

    def test_rewrite_validation_api_requires_original_graph_context(self) -> None:
        self.assertTrue(hasattr(graph_validation, "validate_rewritten_graph"))
        validator = getattr(graph_validation, "validate_rewritten_graph")

        with self.assertRaises(TypeError):
            validator(Graph.from_dict(valid_graph()))

    def test_require_valid_graph_raises_with_all_deterministically_ordered_violations(self) -> None:
        payload = valid_graph()

        with self.assertRaises(GraphValidationError) as caught:
            require_valid_graph(payload)

        codes = [violation.code for violation in caught.exception.violations]
        self.assertEqual(codes, sorted(codes))


if __name__ == "__main__":
    unittest.main()
