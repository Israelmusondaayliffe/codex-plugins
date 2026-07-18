"""Artifact provenance and integrity contracts."""

from __future__ import annotations

import hashlib
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from scripts.graph_engine.artifacts import (
    ArtifactIntegrityError,
    ArtifactRegistry,
    ArtifactUnavailableError,
    UnsafeArtifactPathError,
    resolve_artifact_path,
)
from scripts.graph_engine.events import EventStore, WriterAuthorityError


TIMESTAMP = "2026-07-18T12:00:00Z"


class ArtifactRegistryTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = TemporaryDirectory()
        self.addCleanup(self.temporary_directory.cleanup)
        self.run_directory = Path(self.temporary_directory.name)
        self.store = EventStore(self.run_directory, "run-001")
        self.registry = ArtifactRegistry(self.run_directory, "run-001", self.store)

    def write_artifact(
        self,
        artifact_id: str = "art-000001",
        node_id: str = "researcher",
        content: bytes = b"verified evidence",
    ) -> str:
        relative = f"artifacts/{node_id}/{artifact_id}.md"
        path = self.run_directory / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content)
        return relative

    def register(
        self,
        artifact_id: str = "art-000001",
        node_id: str = "researcher",
        *,
        artifact_type: str = "verified-research",
        supersedes: str | None = None,
    ):
        relative = self.write_artifact(artifact_id, node_id)
        return self.registry.register(
            artifact_id=artifact_id,
            node_id=node_id,
            graph_version=1,
            artifact_type=artifact_type,
            path=relative,
            media_type="text/markdown",
            supersedes=supersedes,
            evidence=[],
            timestamp=TIMESTAMP,
        )

    def test_safe_path_resolution_returns_the_owned_artifact_path(self) -> None:
        relative = self.write_artifact()

        resolved = resolve_artifact_path(self.run_directory, "researcher", relative)

        self.assertEqual(resolved, (self.run_directory / relative).resolve())

    def test_path_traversal_and_symlink_escape_are_rejected(self) -> None:
        outside = self.run_directory.parent / "outside-artifact.txt"
        outside.write_text("outside")
        self.addCleanup(outside.unlink, missing_ok=True)
        owned_directory = self.run_directory / "artifacts" / "researcher"
        owned_directory.mkdir(parents=True)
        (owned_directory / "escape.txt").symlink_to(outside)

        for path in (
            "../outside-artifact.txt",
            "artifacts/researcher/../../outside-artifact.txt",
            "artifacts/researcher/escape.txt",
        ):
            with self.subTest(path=path), self.assertRaises(UnsafeArtifactPathError):
                resolve_artifact_path(self.run_directory, "researcher", path)

    def test_registration_calculates_sha256_and_emits_an_event(self) -> None:
        artifact = self.register()

        self.assertEqual(artifact.sha256, hashlib.sha256(b"verified evidence").hexdigest())
        self.assertEqual(self.registry.read_all(), (artifact,))
        event = self.store.read_all()[0]
        self.assertEqual(event.type.value, "artifact.registered")
        self.assertEqual(event.payload["artifact"], artifact.to_dict())

    def test_hash_mismatch_is_detected(self) -> None:
        artifact = self.register()
        (self.run_directory / artifact.path).write_text("tampered")

        with self.assertRaisesRegex(ArtifactIntegrityError, "SHA-256 mismatch"):
            self.registry.verify(artifact.artifact_id)

    def test_declared_node_must_own_the_artifact_directory(self) -> None:
        relative = self.write_artifact(node_id="builder")

        with self.assertRaisesRegex(UnsafeArtifactPathError, "outside node 'researcher' ownership"):
            self.registry.register(
                artifact_id="art-000001",
                node_id="researcher",
                graph_version=1,
                artifact_type="verified-research",
                path=relative,
                media_type="text/markdown",
                timestamp=TIMESTAMP,
            )

    def test_invalidated_artifact_cannot_satisfy_activation(self) -> None:
        artifact = self.register()
        self.registry.invalidate(artifact.artifact_id, reason="source withdrawn", timestamp=TIMESTAMP)

        with self.assertRaisesRegex(ArtifactUnavailableError, "invalidated"):
            self.registry.verify(artifact.artifact_id)
        self.assertFalse(self.registry.satisfies_activation(["verified-research"]))
        self.assertEqual(self.store.read_all()[-1].type.value, "artifact.invalidated")

    def test_superseded_artifact_is_inactive_and_replacement_is_active(self) -> None:
        original = self.register()
        replacement = self.register("art-000002", supersedes=original.artifact_id)

        with self.assertRaisesRegex(ArtifactUnavailableError, "superseded"):
            self.registry.verify(original.artifact_id)
        self.assertEqual(self.registry.verify(replacement.artifact_id), replacement)

    def test_missing_corrupt_or_wrongly_owned_artifacts_refuse_activation(self) -> None:
        artifact = self.register()
        self.assertTrue(self.registry.satisfies_activation(["verified-research"]))
        (self.run_directory / artifact.path).unlink()

        self.assertFalse(self.registry.satisfies_activation(["verified-research"]))
        self.assertFalse(self.registry.satisfies_activation(["missing-type"]))

    def test_only_the_controller_can_write_the_registry(self) -> None:
        relative = self.write_artifact()

        with self.assertRaises(WriterAuthorityError):
            self.registry.register(
                artifact_id="art-000001",
                node_id="researcher",
                graph_version=1,
                artifact_type="verified-research",
                path=relative,
                media_type="text/markdown",
                actor_node_id="researcher",
                timestamp=TIMESTAMP,
            )

        self.assertFalse(self.registry.path.exists())


if __name__ == "__main__":
    unittest.main()
