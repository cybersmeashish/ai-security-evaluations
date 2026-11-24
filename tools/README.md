# Reproduce contribution 001

Follow [AGENTS.md](../AGENTS.md). Use the repository-specific OrbStack container and persistent workspace.

```sh
docker --context orbstack exec ai-security-evaluations-dev /workspaces/ai-security-evaluations/runtime/bin/python tools/verify.py --output /workspaces/ai-security-evaluations/work/check
```

AI and post-quantum repositories require their hash-locked optional runtime, described in contribution 001. Final verification runs use the same pinned Python image with the workspace mounted read-only and external networking disabled. Output goes to disposable `/tmp` and is transferred back to `evidence/`. No credentials or Docker socket are mounted.

## Prepare the exact optional Linux aarch64 runtime

Run setup inside the repository container. The following lock pins the tested wheels; other architectures need a separately reviewed lock. Keep wheels and runtime outside source.

```sh
docker --context orbstack exec ai-security-evaluations-dev python -m venv /workspaces/ai-security-evaluations/runtime
docker --context orbstack exec ai-security-evaluations-dev /workspaces/ai-security-evaluations/runtime/bin/python -m pip download --require-hashes -r tools/requirements-aarch64.lock -d /workspaces/ai-security-evaluations/work/wheels
docker --context orbstack exec ai-security-evaluations-dev /workspaces/ai-security-evaluations/runtime/bin/python -m pip install --no-index --find-links /workspaces/ai-security-evaluations/work/wheels --require-hashes -r tools/requirements-aarch64.lock
```

```sh
docker --context orbstack exec ai-security-evaluations-dev /workspaces/ai-security-evaluations/runtime/bin/python tools/prepare_model.py --target /workspaces/ai-security-evaluations/work/models/embedding
```

Prepare downloads during controlled setup; run cached inference with external networking disabled.
