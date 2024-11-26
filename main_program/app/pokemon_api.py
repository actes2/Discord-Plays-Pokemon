"""pokemon_api.py

This file is responsible for setting up our game window.

We leverage the `discord` library to send a constant feed of our emulator screen to a 'edited' message in a specific channel.

This is what is actually leveraged in our Docker instance

## Anticipated .ENV

```
API_KEY=<Your API Key>
BOT_NAME=<Your Bot Name>
CHANNEL_ID=<Your channel ID for the Bot>
```
"""

import pyautogui as pyg
from typing import List
import discord
import asyncio
import threading
import logging
import subprocess
from time import sleep
from dotenv import load_dotenv
import os
import sys

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
logger.addHandler(handler)

# todo - add an enviornment variable for the bots name

if not os.getenv("API_KEY"):
    env_result = load_dotenv()
    if not env_result:
        logger.error("environment failed to load!")
        exit(1)

    logger.info("Environment successfully loaded")


api_key = os.getenv("API_KEY")
channel_id = int(os.getenv("CHANNEL_ID"))
bot_name = os.getenv("BOT_NAME")

message_buffer = []

thread_killer = True

action_queue = []


if sys.platform.startswith("win"):
    operating_system = "windows"
else:
    operating_system = "linux"


def is_game_up() -> bool:
    try:
        subprocess.check_output("wmctrl -lG | grep 'mGBA'", shell=True, text=True).split()
        return True
    except Exception:
        return False


def getwindowrect(window_title="mGBA"):
    if operating_system == "windows":
        try:
            gamewin = pyg.getWindowsWithTitle("mGBA")[0]
            return [gamewin.left + 11, gamewin.top + 76, gamewin.right - 11, gamewin.bottom - 11]
        except Exception:
            return None
    else:
        try:
            output = subprocess.check_output("wmctrl -lG | grep 'mGBA'", shell=True, text=True).split()
            return [int(output[2]), int(output[3]) + 2, int(output[4]), int(output[5]) - 21]
        except Exception:
            return None
        

def action_queue_runner():
    while True:
        while action_queue:
            action = action_queue.pop(0)
            logger.info("Executing: {}".format(action))
            act_on_action(action=action)
            

action_thread = threading.Thread(target=action_queue_runner)
action_thread.start()


def act_on_action(action):
    if action == "!a":
        pyg.keyDown("x")
        sleep(0.1)
        pyg.keyUp("x")
    if action == "!b":
        pyg.keyDown("z")
        sleep(0.1)
        pyg.keyUp("z")
    if action == "!u" or action == "!up":
        pyg.keyDown("up")
        sleep(0.1)
        pyg.keyUp("up")
    if action == "!d" or action == "!down":
        pyg.keyDown("down")
        sleep(0.1)
        pyg.keyUp("down")
    if action == "!l" or action == "!left":
        pyg.keyDown("left")
        sleep(0.1)
        pyg.keyUp("left")
    if action == "!r" or action == "!right":
        pyg.keyDown("right")
        sleep(0.1)
        pyg.keyUp("right")
    if action == "!start":
        pyg.keyDown("enter")
        sleep(0.1)
        pyg.keyUp("enter")
    if action == "!select":
        pyg.keyDown("backspace")
        sleep(0.1)
        pyg.keyUp("backspace")
    if action == ("!lb"):
        pyg.keyDown("a")
        sleep(0.1)
        pyg.keyUp("a")
    if action == ("!rb"):
        pyg.keyDown("s")
        sleep(0.1)
        pyg.keyUp("s")


def perform_game_action(action):
    if "+" in action:
        b_action = action.split("+")
        times = int(b_action[1])
        if times > 10:
            times = 10
        for _ in range(0, times):
            action_queue.append(b_action[0])
    else:
        action_queue.append(action)


def check_game_action(action: str):
    keywords = ("!a", "!b", "!start", "!select", "!lb", "!rb", "!u", "!up", "!d", "!down", "!l", "!left", "!r", "!right")
    if action.startswith(keywords):
        perform_game_action(action)


class DiscordClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.skipper = False
        self.command = ""

    async def game(self):
        """Game Runner

        In this method, we render our game, by screenshotting our docker instances XSession, while cropping the game.

        We then take this and edit our existing message, to pretend to be a "screen" of sorts.
        """

        while True:
            channel = self.get_channel(channel_id)
            msgcnt = 0
            all_messages: List[discord.Message] = []

            async for x in channel.history(limit=None):
                msgcnt += 1
                all_messages.append(x)

            gamewin = getwindowrect()
            if gamewin:

                if operating_system == "windows":
                    screen = pyg.screenshot().crop(gamewin)
                else:
                    screen = pyg.screenshot(region=(gamewin))

                screen.save("frame.png")

                if msgcnt > 1:
                    for msg in all_messages:
                        if not msg.author.name == bot_name and str(msg.content).startswith("!"):
                            t = threading.Thread(target=check_game_action, kwargs={"action": str(msg.content)})
                            t.start()
                    await self.fastnuke()

                if msgcnt == 0:
                    await channel.send(file=discord.File("frame.png"))

                if msgcnt == 1:
                    l_msg = all_messages[0]
                    await l_msg.edit(attachments=[discord.File("frame.png")], content="Commands:\n\n!a !b !start !select !lb !rb !up !down !left !right\n\nIf you tag a + after a command followed by a number ex: 'up+5' the bot will run that command that many times!\n\n")

                msgcnt = 0
                all_messages: List[discord.Message] = []

                async for x in channel.history(limit=None):
                    msgcnt += 1
                    all_messages.append(x)

                for msg in all_messages:
                    if not msg.author.name == bot_name and str(msg.content).startswith("!"):
                        t = threading.Thread(target=check_game_action, kwargs={"action": str(msg.content)})
                        t.start()
                await self.fastnuke()
            else:
                logger.error("Failed to capture game window!")

    # fast nuke is for our refresh, hence we're skipping our own stuff, since well if we edit our last message we're chilling.
    async def fastnuke(self):
        logger.info("Wiping Frame")
        channel = self.get_channel(channel_id)
        msgcnt = 0
        all_messages: List[discord.Message] = []

        async for x in channel.history(limit=None):
            msgcnt += 1
            all_messages.append(x)
        for msg in all_messages:
            if msgcnt > 1:
                await msg.delete()
            msgcnt -= 1

    async def nuke(self):
        logger.info("Nuking channel")
        channel = self.get_channel(channel_id)
        await channel.send("Nuking the entire channel in 5")
        await asyncio.sleep(5)
        
        async for i in channel.history(limit=None):
            await i.delete()

    async def screenshot(self):
        logger.info("Taking screenshot")
        channel = self.get_channel(channel_id)

        gamewin = getwindowrect()
        if gamewin:
            if operating_system == "windows":
                screen = pyg.screenshot().crop(gamewin)
            else:
                screen = pyg.screenshot(region=(gamewin))
            screen.save("frame.png")

            frame = await channel.send(file=discord.File("frame.png"))
            await asyncio.sleep(3)
            await frame.delete()
        else:
            logger.info("Failed to capture game window!")
        
    async def on_ready(self):
        logger.info("Ready for action, running:{}".format(self.command))
        channel = self.get_channel(channel_id)
        
        if "/game" in self.command:
            await self.game()

        if "/nuke" in self.command:
            await self.nuke()
        
        if "/ss" in self.command:
            await self.screenshot()

        if "/whoami" in self.command:
            msg = await channel.send("whoami?")
            logger.info(msg.author.name)
            await msg.delete()

        if "/send-" in self.command:
            
            breakdown = self.command.split("-")
            breakdown.pop(0)

            messages = []

            for msg in breakdown:
                logger.info("message sent:{}".format(msg))
                messages.append(await channel.send(msg))

            await asyncio.sleep(5)

            for y in messages:
                await y.delete()
                
        logger.info("Thread has finished, closing connection")
        
        await self.http.connector.close()
        await self.http.close()
        await self.close()


def disc_Thread(command):
    client = DiscordClient(intents=discord.Intents.default())
    client.command = command
    client.run(api_key, reconnect=False, log_handler=None)


def command_and_wait(command):
    thread = threading.Thread(target=disc_Thread, kwargs={"command": command})
    thread.start()


def game_runner():
    while thread_killer:
        logger.info("\ninit_game_loop\n")
        intents = discord.Intents.default()
        intents.message_content = True

        client = DiscordClient(intents=intents)
        client.command = "/game"
        client.run(api_key, reconnect=False, log_handler=None)

    logger.info("\ngame_loop_exited!\n")


def first_time_setup():
    disc_api_key = input("Enter bots api key:")
    chan = input("Enter channel id:")

    with open("/app/.env", "r") as file:
        lines = file.readlines()

    with open("/app/.env", "w") as file:
        for x, line in enumerate(lines):

            if line.startswith("API_KEY="):
                lines[x] = f"API_KEY={disc_api_key}"

            if line.startswith("CHANNEL_ID="):
                lines[x] = f"CHANNEL_ID={chan}"
    

def start_game_window() -> bool:
    try:
        subprocess.check_output("/squashfs-root/AppRun /game/pkmn_ultravhak.gba &", shell=True, text=True)
        return True
    except Exception as e:
        logger.error("Failed to start subprocess:{}".format(e))
        return False


def main():
    logger.info("init")

    thread_killer = False

    # To auto start the game-render loop and bot just run: docker run -it -p 8894:8894 -e AUTO="start" poke_vnc
    auto_start = os.getenv("AUTO")

    while True:
        if auto_start == "start":
            message = "/game"
        else:
            message = input("Message here:")
        
        if message == "/help":
            tutorial = """
            Pokemon_API driver for our container:

            commands:

            /first:\t is for configuring the API-KEY And Channel_ID in the local .env

            /debug:\t is a dry-run /game. It just runs one frame and does all the game things.

            /kill:\t I'm not even sure this works? It's a variable hardstop for telling all returning threads to commit neck.

            /nuke:\t Deletes all messages in the channel in .env

            /ss:\t Takes a screenshot and then removes it after 5 seconds

            /exit:\t Exits the application and container

            /send-#input#:\t Sends a message to the .env channel, which is delimited by -'s. Then deletes it after 5 seconds

            /game:\t Runs our 'game-render-loop'
            
            """

            logger.info(tutorial)

        if message == "/debug":
            intents = discord.Intents.default()
            intents.message_content = True

            client = DiscordClient(intents=intents)
            client.command = "/game"
            client.run(api_key, reconnect=False)

        if message == "/whoami":
            command_and_wait(message)

        if message == '/kill':
            thread_killer = False
            logger.info("Killing game thread!!")
        
        if message == "/ss":
            command_and_wait(message)

        if message == "/nuke":
            command_and_wait(message)

        if "/send-" in message:
            command_and_wait(message)

        if message == "/exit":
            return
        
        if message == "/start_window":
            thread = threading.Thread(target=start_game_window)
            thread.start()

        if message == "/game":
            if not is_game_up:
                thread = threading.Thread(target=start_game_window)
                thread.start()

            if is_game_up:
                if not thread_killer:
                    thread_killer = True

                    thread = threading.Thread(target=game_runner)
                    thread.start()
                    logger.info("Starting game thread!")
                else:
                    logger.info("Game thread already started!!")
            else:
                logger.info("Game appears to actually not be up!")
                logger.info("run /start_window and try again")

        if message == "/first":
            first_time_setup()
                
                
if __name__ == "__main__":
    logger.info(f"Operating system is:{operating_system}")
    main()
