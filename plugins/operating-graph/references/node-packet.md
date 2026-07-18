# Node Packet

Create an immutable `packet.json` before dispatch:

```json
{
  "runId": "run identifier",
  "graphVersion": 1,
  "epoch": 1,
  "node": {},
  "goal": {},
  "requiredInputs": [],
  "availableArtifacts": [],
  "successCriteria": [],
  "outputDirectory": "absolute permitted directory",
  "constraints": [
    "Do not modify graph state.",
    "Do not modify another node's files.",
    "Do not perform external side effects without explicit approval.",
    "Return uncertainty and blockers explicitly."
  ]
}
```

Require the worker result to contain `nodeId`, `status`, `summary`, `artifactPaths`, `evidence`, `unresolvedIssues`, and `recommendedSignals`. Validate node identity, status, artifact ownership, hashes, required outputs, and evidence before transitioning the node.

Register valid artifacts with `python3 scripts/graphctl.py register-artifact <run-directory> <node-id> <artifact-type> <path>`. Reject paths outside the run directory or outside the node's artifact directory.
