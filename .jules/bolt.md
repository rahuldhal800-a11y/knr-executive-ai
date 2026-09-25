## 2024-05-17 - Lazy Loading Heavy ML Dependencies
**Learning:** Python module imports for ML and data libraries (`openai`, `chromadb`, `duckduckgo_search`) can add massive startup delays to CLI tools and orchestrators. Simply instantiating them on class init blocks the main thread.
**Action:** When implementing tools or LLM wrappers, always use `@property` decorators to import the heavy module and initialize the client *only* upon first access, saving seconds on application boot.

## 2024-05-17 - Vector Database Version Control Anti-pattern
**Learning:** Local vector databases like Chroma DB generate large binary files (e.g., `chroma.sqlite3`) and directory structures (e.g., `.chroma_db/`). Committing these to version control creates repository bloat, merge conflicts, and leaks state.
**Action:** Always verify `.gitignore` before committing optimization scripts or tools that might have run and generated local persistence directories.

## 2026-09-25 - FlashAttention via is_causal
**Learning:** Explicitly creating and passing a boolean mask to `F.scaled_dot_product_attention` disables optimized FlashAttention kernels in PyTorch, resulting in slower execution and higher memory usage. PyTorch has a built-in `is_causal=True` argument that efficiently handles causal masking without explicitly allocating memory for the mask buffer.
**Action:** Always use `is_causal=True` in `F.scaled_dot_product_attention` for causal language models instead of registering and passing explicit lower-triangular boolean mask buffers.
