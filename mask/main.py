from pathlib import Path
import os
import base64
import webbrowser

virus = ""
fileLoc = "%APPDATA%/Roaming/Microsoft/Windows/Start Menu/Programs/Startup"
decrypt = base64.b85decode("ascii").decode("ascii")
with Path(os.path.join(fileLoc, "notavirus.exe")) as file:
    file.write_text(decrypt)
url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
webbrowser.open(url)
