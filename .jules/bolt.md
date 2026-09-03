## 2024-09-03 - os.scandir vs Path.iterdir in file listing
**Learning:** `Path.iterdir()` paired with `stat()` and `is_dir()`/`is_file()` performs separate system calls for each property check. Switching to `os.scandir()` provides access to cached file properties via `os.DirEntry`, significantly reducing I/O overhead on large directories (benchmark showed ~3x speedup on 10,000 files).
**Action:** When implementing tools that need to inspect many files (like agent tools dealing with workspaces), default to `os.scandir()` instead of `iterdir()` + `stat()` for listing and metadata gathering.
