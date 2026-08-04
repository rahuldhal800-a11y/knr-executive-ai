# KNR Executive AI v0.2

This project implements a terminal-based filesystem "AI" (no AI used) called KNR Executive AI v0.2.

It provides a small interactive shell to perform filesystem operations. The implementation uses Python's pathlib and shutil and rich for colored terminal output.

Usage

Run the terminal app:

python3 -m app.main

Commands

- help
  Show the help screen.

- list [path]
  List files and folders in the given path (relative to where you started the program). Example: list or list Test

- create folder <folder>
  Create a folder (and any missing parents). Example: create folder Test

- create file <file>
  Create an empty file. Example: create file notes.txt

- read <file>
  Display contents of a file. Example: read notes.txt

- write <file> <text>
  Overwrite a file with text. If the file or parents do not exist, they will be created. Example: write notes.txt "Hello Rahul"

- append <file> <text>
  Append text to a file. Example: append notes.txt "Welcome"

- rename <old> <new>
  Rename a file or folder inside the working directory. Example: rename notes.txt note.txt

- move <old> <new>
  Move a file or folder. Example: move backup.txt Backup/backup.txt

- copy <old> <new>
  Copy a file or folder. Copying directories requires the destination to not already exist. Example: copy note.txt backup.txt

- delete <file_or_folder>
  Delete a file or folder (recursively for folders). Example: delete backup.txt

- clear
  Clear the terminal screen.

- exit
  Exit the program.

Examples (test flow)

1. create folder Test
2. create file notes.txt
3. write notes.txt Hello
4. append notes.txt Rahul
5. read notes.txt
6. rename notes.txt note.txt
7. copy note.txt backup.txt
8. move backup.txt Backup/backup.txt
9. delete note.txt
10. list

Notes

- All paths are resolved relative to the directory where the program is started and the tool prevents operations outside that directory for safety.
- The app uses the `rich` library for colored output. See requirements.txt.
