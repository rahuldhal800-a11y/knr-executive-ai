import os
from pathlib import Path

from app.tools.file_tool import FileTool


def test_file_tool_workflow(tmp_path: Path):
    # Initialize tool with isolated tmp_path
    base = tmp_path
    tool = FileTool(base)

    # 1. create folder Test
    r = tool.create_folder("Test")
    assert r["ok"], r
    assert (base / "Test").is_dir()

    # 2. create file notes.txt
    r = tool.create_file("notes.txt")
    assert r["ok"], r
    assert (base / "notes.txt").is_file()

    # 3. write notes.txt Hello
    r = tool.write_file("notes.txt", "Hello")
    assert r["ok"], r

    # 4. append notes.txt Rahul
    r = tool.append_file("notes.txt", "Rahul")
    assert r["ok"], r

    # 5. read notes.txt
    r = tool.read_file("notes.txt")
    assert r["ok"], r
    assert r.get("content") == "HelloRahul"

    # 6. rename notes.txt note.txt
    r = tool.rename("notes.txt", "note.txt")
    assert r["ok"], r
    assert not (base / "notes.txt").exists()
    assert (base / "note.txt").exists()

    # 7. copy note.txt backup.txt
    r = tool.copy("note.txt", "backup.txt")
    assert r["ok"], r
    assert (base / "backup.txt").exists()

    # 8. move backup.txt Backup/backup.txt
    r = tool.move("backup.txt", "Backup/backup.txt")
    assert r["ok"], r
    assert not (base / "backup.txt").exists()
    assert (base / "Backup" / "backup.txt").exists()

    # 9. delete note.txt
    r = tool.delete("note.txt")
    assert r["ok"], r
    assert not (base / "note.txt").exists()

    # 10. list
    r = tool.list_files()
    assert r["ok"], r
    # Backup directory should be present in listing
    items = [i["name"] for i in r.get("items", [])]
    assert "Backup" in items
