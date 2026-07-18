"""Deterministic scheduler contracts for Operating Graph runtimes."""

from __future__ import annotations

from dataclasses import replace
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from scripts.graph_engine.artifacts import ArtifactRegistry
from scripts.graph_engine.constants import ApprovalStatus, NodeStatus, RunStatus
from scripts.graph_engine.events import EventStore
from scripts.graph_engine.models import Approval, Graph, NodeRuntimeState, RuntimeState
from scripts.graph_engine.scheduler import can_advance_epoch, detect_deadlock, get_ready_nodes


TIMESTAMP = "2026-07-18T12:00:00Z"


def node(
    node_id: str,
    *,
    priority: int = 50,
    critical: bool = True,
    enabled: bool = True,
    inputs: list[str] | None = None,
    max_attempts: int = 2,
) -> dict[str, object]:
    return {
        "id": node_id,
        "kind": "worker",
        "label": node_id.title(),
        "purpose": f"Run {node_id}.",
        "enabled": enabled,
        "critical": critical,
        "priority": priority,
        "execution": {"mode": "inline", "skill": None, "modelHint": None},
        "capabilities": ["analysis"],
        "inputs": [
            {"artifactType": artifact_type, "required": True}
            for artifact_type in (inputs or [])
        ],
        "outputs": [],
        "successCriteria": ["Work is complete."],
        "budget": {"maxAttempts": max_attempts, "workUnits": 1},
        "localLoop": {
            "enabled": False,
            "maxIterations": 1,
            "sequence": [],
            "stopCondition": "complete",
        },
    }


def edge(
    edge_id: str,
    source: str,
    target: str,
    *,
    temporal: str = "same_epoch",
    artifacts: list[str] | None = None,
    approvals: list[str] | None = None,
    node_states: list[dict[str, str]] | None = None,
    mode: str = "all",
    required: bool = True,
    edge_artifact_types: list[str] | None = None,
) -> dict[str, object]:
    return {
        "id": edge_id,
        "source": source,
        "target": target,
        "kind": "assign",
        "enabled": True,
        "required": required,
        "temporal": temporal,
        "artifactTypes": edge_artifact_types or [],
        "activation": {
            "mode": mode,
            "nodeStates": node_states or [],
            "artifacts": artifacts or [],
            "approvals": approvals or [],
        },
    }


def graph(
    nodes: list[dict[str, object]],
    edges: list[dict[str, object]] | None = None,
    *,
    max_concurrency: int = 8,
    max_node_runs: int = 30,
    max_epochs: int = 3,
    default_attempts: int = 2,
) -> Graph:
    return Graph.from_dict(
        {
            "schemaVersion": "1.0",
            "graphId": "scheduler-test",
            "name": "Scheduler Test",
            "goal": {
                "statement": "Schedule deterministically.",
                "deliverables": [],
                "completionCriteria": ["All critical nodes finish."],
                "authorityNodeId": "authority",
            },
            "limits": {
                "maxConcurrentWorkers": max_concurrency,
                "maxNodeRuns": max_node_runs,
                "maxGraphVersions": 5,
                "maxEpochs": max_epochs,
                "maxAutoRewrites": 1,
                "defaultMaxAttempts": default_attempts,
            },
            "nodes": nodes,
            "edges": edges or [],
            "rewritePolicy": {
                "automaticRiskLevels": ["low"],
                "approvalRiskLevels": ["medium", "high"],
                "prohibitedMutations": [],
            },
            "metadata": {"createdBy": "tests", "createdAt": TIMESTAMP},
        }
    )


def state(
    statuses: dict[str, NodeStatus],
    *,
    epoch: int = 1,
    attempts: dict[str, int] | None = None,
    completed_epochs: dict[str, int] | None = None,
    total_node_runs: int = 0,
) -> RuntimeState:
    return RuntimeState(
        run_id="run-001",
        graph_id="scheduler-test",
        graph_version=1,
        epoch=epoch,
        status=RunStatus.RUNNING,
        node_states={
            node_id: NodeRuntimeState(
                node_id=node_id,
                status=node_status,
                attempts=(attempts or {}).get(node_id, 0),
                completed_epoch=(completed_epochs or {}).get(node_id),
            )
            for node_id, node_status in statuses.items()
        },
        total_node_runs=total_node_runs,
    )


def approval(approval_id: str, status: ApprovalStatus) -> Approval:
    return Approval.from_dict(
        {
            "approvalId": approval_id,
            "runId": "run-001",
            "subjectType": "external-action",
            "subjectId": approval_id,
            "requestedBy": "controller",
            "requiredFrom": "authority",
            "status": status.value,
            "requestedAt": TIMESTAMP,
        }
    )


class SchedulerTests(unittest.TestCase):
    def test_activation_requires_declared_node_state_conditions(self) -> None:
        runtime_graph = graph(
            [node("producer"), node("consumer")],
            [
                edge(
                    "producer-consumer",
                    "producer",
                    "consumer",
                    node_states=[{"nodeId": "producer", "status": "succeeded"}],
                )
            ],
        )
        waiting = state(
            {"producer": NodeStatus.PENDING, "consumer": NodeStatus.PENDING}
        )
        satisfied = state(
            {"producer": NodeStatus.SUCCEEDED, "consumer": NodeStatus.PENDING},
            completed_epochs={"producer": 1},
        )

        self.assertEqual([item.id for item in get_ready_nodes(runtime_graph, waiting)], ["producer"])
        self.assertEqual([item.id for item in get_ready_nodes(runtime_graph, satisfied)], ["consumer"])

    def test_any_activation_mode_accepts_one_satisfied_condition(self) -> None:
        runtime_graph = graph(
            [node("producer"), node("consumer")],
            [
                edge(
                    "producer-consumer",
                    "producer",
                    "consumer",
                    node_states=[{"nodeId": "producer", "status": "failed"}],
                    approvals=["approval-1"],
                    mode="any",
                )
            ],
        )
        runtime_state = state(
            {"producer": NodeStatus.SUCCEEDED, "consumer": NodeStatus.PENDING},
            completed_epochs={"producer": 1},
        )

        ready = get_ready_nodes(
            runtime_graph,
            runtime_state,
            approvals=[approval("approval-1", ApprovalStatus.GRANTED)],
        )

        self.assertEqual([item.id for item in ready], ["consumer"])

    def test_approval_dependencies_require_granted_status(self) -> None:
        runtime_graph = graph(
            [node("publish")],
            [edge("approval-edge", "publish", "publish", approvals=["approval-1"])],
        )
        runtime_state = state({"publish": NodeStatus.PENDING})

        self.assertEqual(
            get_ready_nodes(
                runtime_graph,
                runtime_state,
                approvals=[approval("approval-1", ApprovalStatus.PENDING)],
            ),
            (),
        )
        self.assertEqual(
            [item.id for item in get_ready_nodes(
                runtime_graph,
                runtime_state,
                approvals=[approval("approval-1", ApprovalStatus.GRANTED)],
            )],
            ["publish"],
        )

    def test_artifact_dependencies_use_registry_integrity(self) -> None:
        with TemporaryDirectory() as directory:
            run_directory = Path(directory)
            artifact_path = run_directory / "artifacts" / "producer" / "art-000001.txt"
            artifact_path.parent.mkdir(parents=True)
            artifact_path.write_text("valid")
            store = EventStore(run_directory, "run-001")
            registry = ArtifactRegistry(run_directory, "run-001", store)
            registry.register(
                artifact_id="art-000001",
                node_id="producer",
                graph_version=1,
                artifact_type="research",
                path="artifacts/producer/art-000001.txt",
                media_type="text/plain",
                timestamp=TIMESTAMP,
            )
            runtime_graph = graph([node("consumer", inputs=["research"])])
            runtime_state = state({"consumer": NodeStatus.PENDING})

            self.assertEqual(
                [item.id for item in get_ready_nodes(
                    runtime_graph, runtime_state, artifact_registry=registry
                )],
                ["consumer"],
            )
            artifact_path.write_text("corrupt")
            self.assertEqual(
                get_ready_nodes(runtime_graph, runtime_state, artifact_registry=registry),
                (),
            )

    def test_required_edge_artifacts_cannot_be_bypassed_by_any_activation(self) -> None:
        runtime_graph = graph(
            [node("publish")],
            [
                edge(
                    "publish-approval",
                    "publish",
                    "publish",
                    approvals=["approval-1"],
                    mode="any",
                    edge_artifact_types=["verified-report"],
                )
            ],
        )
        runtime_state = state({"publish": NodeStatus.PENDING})

        ready = get_ready_nodes(
            runtime_graph,
            runtime_state,
            approvals=[approval("approval-1", ApprovalStatus.GRANTED)],
        )

        self.assertEqual(ready, ())

    def test_sorting_uses_priority_then_critical_then_downstream_release_count_then_id(self) -> None:
        runtime_graph = graph(
            [
                node("high", priority=100, critical=False),
                node("critical-many", priority=50),
                node("critical-few", priority=50),
                node("alpha", priority=50, critical=False),
                node("beta", priority=50, critical=False),
                node("downstream-one"),
                node("downstream-two"),
            ],
            [
                edge("many-one", "critical-many", "downstream-one", required=True),
                edge("many-two", "critical-many", "downstream-two", required=True),
                edge("few-one", "critical-few", "downstream-one", required=True),
            ],
        )
        runtime_state = state(
            {node_id: NodeStatus.PENDING for node_id in (
                "high", "critical-many", "critical-few", "alpha", "beta",
                "downstream-one", "downstream-two",
            )}
        )

        first = tuple(item.id for item in get_ready_nodes(runtime_graph, runtime_state))
        second = tuple(item.id for item in get_ready_nodes(runtime_graph, runtime_state))

        self.assertEqual(
            first,
            ("high", "critical-many", "critical-few", "alpha", "beta"),
        )
        self.assertEqual(second, first)

    def test_downstream_sort_counts_only_incomplete_targets(self) -> None:
        runtime_graph = graph(
            [
                node("many-complete"),
                node("one-incomplete"),
                node("done-one"),
                node("done-two"),
                node("waiting"),
            ],
            [
                edge("many-done-one", "many-complete", "done-one"),
                edge("many-done-two", "many-complete", "done-two"),
                edge("one-waiting", "one-incomplete", "waiting"),
            ],
        )
        runtime_state = state(
            {
                "many-complete": NodeStatus.PENDING,
                "one-incomplete": NodeStatus.PENDING,
                "done-one": NodeStatus.SUCCEEDED,
                "done-two": NodeStatus.SUCCEEDED,
                "waiting": NodeStatus.PENDING,
            },
            completed_epochs={"done-one": 1, "done-two": 1},
        )

        ready = tuple(item.id for item in get_ready_nodes(runtime_graph, runtime_state))

        self.assertEqual(ready[:2], ("one-incomplete", "many-complete"))

    def test_concurrency_is_clamped_by_graph_and_detected_slots(self) -> None:
        runtime_graph = graph(
            [node("a"), node("b"), node("c")], max_concurrency=2
        )
        runtime_state = state(
            {"a": NodeStatus.PENDING, "b": NodeStatus.PENDING, "c": NodeStatus.PENDING}
        )

        self.assertEqual(
            len(get_ready_nodes(runtime_graph, runtime_state, detected_available_worker_slots=10)),
            2,
        )
        self.assertEqual(
            len(get_ready_nodes(runtime_graph, runtime_state, detected_available_worker_slots=1)),
            1,
        )
        self.assertEqual(
            get_ready_nodes(runtime_graph, runtime_state, detected_available_worker_slots=0),
            (),
        )

    def test_next_epoch_dependency_waits_for_the_epoch_boundary(self) -> None:
        runtime_graph = graph(
            [node("signal"), node("revision")],
            [
                edge(
                    "feedback",
                    "signal",
                    "revision",
                    temporal="next_epoch",
                    node_states=[{"nodeId": "signal", "status": "succeeded"}],
                )
            ],
        )
        epoch_one = state(
            {"signal": NodeStatus.SUCCEEDED, "revision": NodeStatus.PENDING},
            epoch=1,
            completed_epochs={"signal": 1},
        )
        epoch_two = replace(epoch_one, epoch=2)

        self.assertEqual(get_ready_nodes(runtime_graph, epoch_one), ())
        self.assertTrue(can_advance_epoch(runtime_graph, epoch_one))
        self.assertEqual([item.id for item in get_ready_nodes(runtime_graph, epoch_two)], ["revision"])

    def test_retry_and_overall_run_budgets_gate_readiness(self) -> None:
        runtime_graph = graph([node("retry", max_attempts=2)], max_node_runs=2)
        retryable = state(
            {"retry": NodeStatus.FAILED}, attempts={"retry": 1}, total_node_runs=1
        )
        exhausted_node = state(
            {"retry": NodeStatus.FAILED}, attempts={"retry": 2}, total_node_runs=1
        )
        exhausted_run = state(
            {"retry": NodeStatus.FAILED}, attempts={"retry": 1}, total_node_runs=2
        )

        self.assertEqual([item.id for item in get_ready_nodes(runtime_graph, retryable)], ["retry"])
        self.assertEqual(get_ready_nodes(runtime_graph, exhausted_node), ())
        self.assertEqual(get_ready_nodes(runtime_graph, exhausted_run), ())

    def test_incomplete_graph_without_runnable_or_epoch_work_is_a_deadlock(self) -> None:
        runtime_graph = graph(
            [node("producer", max_attempts=1), node("consumer")],
            [
                edge(
                    "producer-consumer",
                    "producer",
                    "consumer",
                    node_states=[{"nodeId": "producer", "status": "succeeded"}],
                )
            ],
        )
        deadlocked = state(
            {"producer": NodeStatus.FAILED, "consumer": NodeStatus.PENDING},
            attempts={"producer": 1},
        )
        progressing = state(
            {"producer": NodeStatus.RUNNING, "consumer": NodeStatus.PENDING},
            attempts={"producer": 1},
        )
        complete = state(
            {"producer": NodeStatus.SUCCEEDED, "consumer": NodeStatus.SUCCEEDED},
            completed_epochs={"producer": 1, "consumer": 1},
        )

        report = detect_deadlock(runtime_graph, deadlocked)
        self.assertIsNotNone(report)
        self.assertEqual(report.blocked_node_ids, ("consumer", "producer"))
        self.assertIsNone(detect_deadlock(runtime_graph, progressing))
        self.assertIsNone(detect_deadlock(runtime_graph, complete))


if __name__ == "__main__":
    unittest.main()
