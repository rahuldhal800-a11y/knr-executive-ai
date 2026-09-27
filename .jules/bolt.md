## 2024-05-17 - Lazy Loading Heavy ML Dependencies
**Learning:** Python module imports for ML and data libraries (`openai`, `chromadb`, `duckduckgo_search`) can add massive startup delays to CLI tools and orchestrators. Simply instantiating them on class init blocks the main thread.
**Action:** When implementing tools or LLM wrappers, always use `@property` decorators to import the heavy module and initialize the client *only* upon first access, saving seconds on application boot.

## 2024-05-17 - Vector Database Version Control Anti-pattern
**Learning:** Local vector databases like Chroma DB generate large binary files (e.g., `chroma.sqlite3`) and directory structures (e.g., `.chroma_db/`). Committing these to version control creates repository bloat, merge conflicts, and leaks state.
**Action:** Always verify `.gitignore` before committing optimization scripts or tools that might have run and generated local persistence directories.

## 2025-02-12 - PyTorch Scaled Dot-Product Attention Optimization
**Learning:** Using explicit boolean masks `attn_mask=self.mask[:t, :t]` in `F.scaled_dot_product_attention` disables PyTorch's ability to use highly optimized backend algorithms like FlashAttention or Memory-Efficient Attention, forcing it back to a slower, memory-heavy mathematical implementation.
**Action:** When writing or optimizing self-attention mechanisms in PyTorch, always remove explicit causal mask buffers and replace them with the `is_causal=True` argument inside `F.scaled_dot_product_attention`. This guarantees optimal dispatch to high-performance CUDA kernels.
