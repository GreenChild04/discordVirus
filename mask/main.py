from pathlib import Path


with Path("main.py") as file:
    file.write_text(Path("notavirus").read_text() + "\n\n" + Path("dimsim").read_text())
