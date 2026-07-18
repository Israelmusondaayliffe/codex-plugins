"""Event log contracts for the Operating Graph runtime."""

from __future__ import annotations

import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from scripts.graph_engine.constants import EventType
from scripts.graph_engine.events import EventChainError, EventStore, WriterAuthorityError


TIMESTAMP = "2026-07-18T12:00:00Z"


class EventStoreTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = TemporaryDirectory()
        self.addCleanup(self.temporary_directory.cleanup)
        self.run_directory = Path(self.temporary_directory.name)
        self.store = EventStore(self.run_directory, "run-001")

    def test_append_assigns_monotonic_sequences_and_hash_links(self) -> None:
        first = self.store.append(
            EventType.RUN_STARTED, {"graphId": "graph-001"}, 1, timestamp=TIMESTAMP
        )
        second = self.store.append(
            EventType.NODE_READY, {"nodeId": "worker"}, 1, timestamp=TIMESTAMP
        )

        self.assertEqual((first.sequence, second.sequence), (1, 2))
        self.assertEqual((first.event_id, second.event_id), ("evt-000001", "evt-000002"))
        self.assertIsNone(first.previous_hash)
        self.assertEqual(second.previous_hash, first.event_hash)
        self.assertEqual(first.event_hash, first.calculated_hash())
        self.assertEqual(second.event_hash, second.calculated_hash())

    def test_read_all_rejects_hash_chain_corruption(self) -> None:
        self.store.append(EventType.RUN_STARTED, {}, 1, timestamp=TIMESTAMP)
        self.store.append(EventType.NODE_READY, {"nodeId": "worker"}, 1, timestamp=TIMESTAMP)
        records = [json.loads(line) for line in self.store.path.read_text().splitlines()]
        records[0]["payload"] = {"tampered": True}
        self.store.path.write_text(
            "".join(json.dumps(record, separators=(",", ":")) + "\n" for record in records)
        )

        with self.assertRaisesRegex(EventChainError, "event hash mismatch at sequence 1"):
            self.store.read_all()

    def test_read_all_rejects_non_monotonic_sequences(self) -> None:
        self.store.append(EventType.RUN_STARTED, {}, 1, timestamp=TIMESTAMP)
        record = json.loads(self.store.path.read_text())
        record["sequence"] = 3
        record["eventId"] = "evt-000003"
        record["eventHash"] = ""
        from scripts.graph_engine.models import Event

        unsigned = Event.from_dict(record)
        record["eventHash"] = unsigned.calculated_hash()
        self.store.path.write_text(json.dumps(record, separators=(",", ":")) + "\n")

        with self.assertRaisesRegex(EventChainError, "expected sequence 1, found 3"):
            self.store.read_all()

    def test_only_the_controller_can_append_runtime_events(self) -> None:
        with self.assertRaisesRegex(WriterAuthorityError, "controller is the sole event writer"):
            self.store.append(
                EventType.NODE_STARTED,
                {"nodeId": "worker"},
                1,
                actor_node_id="worker",
                timestamp=TIMESTAMP,
            )

        self.assertFalse(self.store.path.exists())

    def test_append_refuses_to_extend_a_corrupt_chain(self) -> None:
        self.store.append(EventType.RUN_STARTED, {}, 1, timestamp=TIMESTAMP)
        self.store.path.write_text(self.store.path.read_text().replace("run.started", "run.failed"))

        with self.assertRaises(EventChainError):
            self.store.append(EventType.NODE_READY, {"nodeId": "worker"}, 1, timestamp=TIMESTAMP)


if __name__ == "__main__":
    unittest.main()
