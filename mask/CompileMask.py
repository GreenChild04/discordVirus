from pathlib import Path
from sys import *


with Path(argv[1]) as file:
	file.write_text(Path("dimsim").read_text().replace("*", f'"{Path("notavirus").read_text()}"'))