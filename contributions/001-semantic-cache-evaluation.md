# Contribution 001 — Semantic similarity is not permission or query equivalence

**Learned-encoder experiment, 24 November 2026.** A semantic cache can reduce inference calls, but a close embedding is neither a current grant nor proof that two questions have the same important meaning.

## Experiment

This contribution runs the exact `sentence-transformers/all-MiniLM-L6-v2` ONNX encoder on sixteen synthetic English question pairs. Six pairs repeat identical text while changing subject/case, purpose, permission epoch, corpus or release metadata. Other pairs change identifiers, amounts, negation or legal notice wording. Five pairs are annotated as equivalent procedural questions.

The model weights/tokenizer are loaded only from the local, checksum-verified cache outside public source. [The manifest](../fixtures/model-manifest.json) records the upstream repository revision and exact artifact hashes. The upstream model declares Apache-2.0; its weights are not redistributed here. [Sentence Transformers' primary model card](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2) explains the encoder's origin and scope.

The experiment compares cosine-only admission with cosine plus explicit scope/critical-field equality across thresholds 0.85, 0.90, 0.95 and 0.97. [Results](../evidence/results.json) and the per-pair CSV show every score and decision. No support answer or tool-using LLM is generated.

## Interpretation

Identical wording can belong to another customer or a revoked permission epoch. The embedding contains the text, not the authoritative access state. Raising a similarity threshold cannot solve those missing inputs. Closely worded changes in numbers or negation must also be assessed as distinct meanings.

The metadata gate is deliberately bounded: annotations are fixture inputs, not outputs of a real identity service, entity recognizer or intent classifier. Low false reuse in this fixture does not prove that production extraction can recover important fields or that all legal meanings are equivalent. Labels were authored for the experiment and not independently adjudicated; this is not a sealed bank benchmark.

## Cache contract to take forward

Authenticate and authorise before probing a scope-specific cache. Bind purpose, case/customer, subject/share group, permission epoch, corpus/index generation, policy/model/prompt release, language and as-of context. Recheck all cited document versions before returning a hit. Default material financial/legal decisions, live balances and sensitive tool actions to a separately reviewed non-reuse path.

Track hit/total, hit/eligible, invalidation, expiry, rejected semantic candidates, quality of served hits and actual cost avoided. A high hit rate is not useful if the answer is stale, unsupported or disclosed to the wrong person.

## Reproduce

Use the repository-specific OrbStack runtime and `tools/requirements-aarch64.lock` for the exact tested Linux aarch64 environment. The canonical model cache is `/workspaces/ai-security-evaluations/work/models/embedding`; obtain only the recorded upstream revision and verify every manifest digest before offline execution. Set `AI_CACHE_MODEL_DIRECTORY` to an equivalent verified cache if needed. Final runs mount the workspace read-only and disable external networking.

Next work should add expert labels, legal/financial semantics, Indian-language pairs, realistic metadata extraction failures and a protected end-to-end cache trial. This contribution establishes a reproducible narrow risk, not general semantic-cache correctness.
