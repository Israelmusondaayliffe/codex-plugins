"""Event-backed state-machine contracts for Operating Graph runs."""

from __future__ import annotations

import json
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch
import unittest

from scripts.graph_engine.constants import NODE_STATUS_TRANSITIONS, NodeStatus, RunStatus
from scripts.graph_engine.events import EventStore, WriterAuthorityError
from scripts.graph_engine.models import NodeRuntimeState, RuntimeState
from scripts.graph_engine.state import (
    IllegalTransitionError,
    RetryRejectedError,
    StateMachine,
    replay_events,
)


TIMESTAMP = "2026-07-18T12:00:00Z"


def initial_state(status: NodeStatus = NodeStatus.PENDING, attempts: int = 0) -> RuntimeState:
    return RuntimeState(
        run_id="run-001",
        graph_id="graph-001",
        graph_version=1,
        epoch=1,
        status=RunStatus.RUNNING,
        node_states={
            "worker": NodeRuntimeState(node_id="worker", status=status, attempts=attempts)
        },
    )


class StateMachineTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = TemporaryDirectory()
        self.addCleanup(self.temporary_directory.cleanup)
        self.run_directory = Path(self.temporary_directory.name)

    def make_machine(
        self, status: NodeStatus = NodeStatus.PENDING, attempts: int = 0
    ) -> StateMachine:
        store = EventStore(self.run_directory, "run-001")
        return StateMachine.create(
            self.run_directory,
            initial_state(status, attempts),
            store,
            timestamp=TIMESTAMP,
        )

    def test_every_declared_node_transition_is_accepted_and_event_backed(self) -> None:
        for source, target in sorted(NODE_STATUS_TRANSITIONS, key=lambda item: (item[0].value, item[1].value)):
            with self.subTest(source=source.value, target=target.value):
                with TemporaryDirectory() as directory:
                    path = Path(directory)
                    store = EventStore(path, "run-001")
                    machine = StateMachine.create(
                        path,
                        initial_state(source, attempts=0),
                        store,
                        timestamp=TIMESTAMP,
                    )
                    machine.transition_node(
                        "worker",
                        target,
                        timestamp=TIMESTAMP,
                        max_attempts=2,
                        required_inputs_exist=True,
                        approval_outstanding=False,
                    )

                    self.assertEqual(machine.state.node_states["worker"].status, target)
                    self.assertEqual(len(store.read_all()), 2)

    def test_representative_illegal_transitions_are_rejected_without_events(self) -> None:
        for source, target in (
            (NodeStatus.PENDING, NodeStatus.RUNNING),
            (NodeStatus.SUCCEEDED, NodeStatus.RUNNING),
            (NodeStatus.CANCELLED, NodeStatus.READY),
        ):
            with self.subTest(source=source.value, target=target.value):
                with TemporaryDirectory() as directory:
                    path = Path(directory)
                    store = EventStore(path, "run-001")
                    machine = StateMachine.create(
                        path, initial_state(source), store, timestamp=TIMESTAMP
                    )
                    with self.assertRaises(IllegalTransitionError):
                        machine.transition_node("worker", target, timestamp=TIMESTAMP)
                    self.assertEqual(len(store.read_all()), 1)

    def test_failed_to_ready_requires_the_complete_retry_contract(self) -> None:
        cases = (
            ({"max_attempts": 1, "required_inputs_exist": True, "approval_outstanding": False}, "attempt budget exhausted"),
            ({"max_attempts": 2, "required_inputs_exist": False, "approval_outstanding": False}, "required inputs are unavailable"),
            ({"max_attempts": 2, "required_inputs_exist": True, "approval_outstanding": True}, "required approval is outstanding"),
        )
        for arguments, message in cases:
            with self.subTest(message=message):
                with TemporaryDirectory() as directory:
                    path = Path(directory)
                    store = EventStore(path, "run-001")
                    machine = StateMachine.create(
                        path, initial_state(NodeStatus.FAILED, attempts=1), store, timestamp=TIMESTAMP
                    )
                    with self.assertRaisesRegex(RetryRejectedError, message):
                        machine.transition_node(
                            "worker", NodeStatus.READY, timestamp=TIMESTAMP, **arguments
                        )
                    self.assertEqual(len(store.read_all()), 1)

    def test_retry_emits_node_retried_and_start_increments_attempt_counters(self) -> None:
        machine = self.make_machine(NodeStatus.FAILED, attempts=1)
        machine.transition_node(
            "worker",
            NodeStatus.READY,
            timestamp=TIMESTAMP,
            max_attempts=2,
            required_inputs_exist=True,
            approval_outstanding=False,
        )
        machine.transition_node("worker", NodeStatus.RUNNING, timestamp=TIMESTAMP)

        events = EventStore(self.run_directory, "run-001").read_all()
        self.assertEqual(events[1].type.value, "node.retried")
        self.assertEqual(machine.state.node_states["worker"].attempts, 2)
        self.assertEqual(machine.state.total_node_runs, 1)

    def test_atomic_state_replace_failure_preserves_the_previous_state_file(self) -> None:
        machine = self.make_machine()
        before = (self.run_directory / "state.json").read_bytes()

        with patch("scripts.graph_engine.state.os.replace", side_effect=OSError("replace failed")):
            with self.assertRaisesRegex(OSError, "replace failed"):
                machine.transition_node("worker", NodeStatus.READY, timestamp=TIMESTAMP)

        self.assertEqual((self.run_directory / "state.json").read_bytes(), before)

    def test_replay_produces_the_same_final_state(self) -> None:
        machine = self.make_machine()
        machine.transition_node("worker", NodeStatus.READY, timestamp=TIMESTAMP)
        machine.transition_node("worker", NodeStatus.RUNNING, timestamp=TIMESTAMP)
        machine.transition_node("worker", NodeStatus.SUCCEEDED, timestamp=TIMESTAMP)

        replayed = replay_events(EventStore(self.run_directory, "run-001").read_all())

        self.assertEqual(replayed.to_dict(), machine.state.to_dict())

    def test_resume_rejects_a_corrupt_chain_before_restoring_state(self) -> None:
        machine = self.make_machine()
        machine.transition_node("worker", NodeStatus.READY, timestamp=TIMESTAMP)
        event_path = self.run_directory / "events.jsonl"
        event_path.write_text(event_path.read_text().replace("node.ready", "node.started"))

        with self.assertRaisesRegex(Exception, "event hash mismatch"):
            StateMachine.resume(
                self.run_directory, EventStore(self.run_directory, "run-001")
            )

    def test_exposed_state_is_a_copy_and_direct_non_controller_mutation_is_rejected(self) -> None:
        machine = self.make_machine()
        exposed = machine.state
        exposed.node_states["worker"] = NodeRuntimeState(
            node_id="worker", status=NodeStatus.SUCCEEDED
        )

        self.assertEqual(machine.state.node_states["worker"].status, NodeStatus.PENDING)
        self.assertEqual(
            json.loads((self.run_directory / "state.json").read_text())["nodeStates"]["worker"]["status"],
            "pending",
        )
        with self.assertRaises(WriterAuthorityError):
            machine.transition_node(
                "worker", NodeStatus.READY, actor_node_id="worker", timestamp=TIMESTAMP
            )


if __name__ == "__main__":
    unittest.main()
