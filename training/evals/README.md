# AEGIS Evaluation Harness

A model release must be measured, not declared "best" by intuition.

Each benchmark case has an `id`, `category`, `prompt`, and expected behavior. Add held-out cases for coding, tool calling, reasoning, factuality, cybersecurity defense, authorization boundaries, and real-world agent tasks.

Recommended release gate: no critical safety/authorization regression; no regression on core agent tasks; documented comparison against the previous release; reproducible benchmark version; published model card and training provenance.
