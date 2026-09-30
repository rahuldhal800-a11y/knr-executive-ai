## 2024-05-17 - Lazy Loading Heavy ML Dependencies
**Learning:** Python module imports for ML and data libraries (`openai`, `chromadb`, `duckduckgo_search`) can add massive startup delays to CLI tools and orchestrators. Simply instantiating them on class init blocks the main thread.
**Action:** When implementing tools or LLM wrappers, always use `@property` decorators to import the heavy module and initialize the client *only* upon first access, saving seconds on application boot.

## 2024-05-17 - Vector Database Version Control Anti-pattern
**Learning:** Local vector databases like Chroma DB generate large binary files (e.g., `chroma.sqlite3`) and directory structures (e.g., `.chroma_db/`). Committing these to version control creates repository bloat, merge conflicts, and leaks state.
**Action:** Always verify `.gitignore` before committing optimization scripts or tools that might have run and generated local persistence directories.
## 2024-05-18 - SDPA is_causal=True CPU/WASM inference edge cases
**Learning:** PyTorch `F.scaled_dot_product_attention` with `is_causal=True` enables memory efficiency and FlashAttention on GPUs, but can actually be slower than explicit masking on CPUs without optimized kernels.
**Action:** Always measure on target hardware. Still keeping the change since the primary use case for this optimization in training/inference involves GPUs where FlashAttention will kick in.
