import pyautogui as pyg
from typing import List
import discord
import asyncio
import threading
import logging
import subprocess
from dotenv import load_dotenv
import os
import sys

load_dotenv()

logger = logging.getLogger()
api_key = os.getenv("DISCORD_API_TOKEN")
channel_id = int(os.getenv("CHANNEL_ID"))

message_buffer = []

thread_killer = True


if sys.platform.startswith("win"):
    operating_system = "windows"
else:
    operating_system = "linux"


def is_game_up() -> bool:
    try:
        subprocess.check_output("wmctrl -lG | grep 'mGBA'", shell=True, text=True).split()
        return True
    except:
        return False
    
    

def getwindowrect(window_title="mGBA"):
    if operating_system == "windows":
        try:
            gamewin = pyg.getWindowsWithTitle("mGBA")[0]
            return [gamewin.left + 11, gamewin.top + 76, gamewin.right - 11, gamewin.bottom - 11]
        except:
            return None
    else:
        try:
            output = subprocess.check_output("wmctrl -lG | grep 'mGBA'", shell=True, text=True).split()
            return [int(output[2]), int(output[3]) + 2, int(output[4]), int(output[5]) - 21]
        except:
            return None


async def act_on_action(action):
    if action == "!a":
        pyg.keyDown("x")
        await asyncio.sleep(0.1)
        pyg.keyUp("x")
    if action == "!b":
        pyg.keyDown("z")
        await asyncio.sleep(0.1)
        pyg.keyUp("z")
    if action == "!u" or action == "!up":
        pyg.keyDown("up")
        await asyncio.sleep(0.1)
        pyg.keyUp("up")
    if action == "!d" or action == "!down":
        pyg.keyDown("down")
        await asyncio.sleep(0.1)
        pyg.keyUp("down")
    if action == "!l" or action == "!left":
        pyg.keyDown("left")
        await asyncio.sleep(0.1)
        pyg.keyUp("left")
    if action == "!r" or action == "!right":
        pyg.keyDown("right")
        await asyncio.sleep(0.1)
        pyg.keyUp("right")
    if action == "!start":
        pyg.keyDown("enter")
        await asyncio.sleep(0.1)
        pyg.keyUp("enter")
    if action == "!select":
        pyg.keyDown("backspace")
        await asyncio.sleep(0.1)
        pyg.keyUp("backspace")
    if action == ("!lb"):
        pyg.keyDown("a")
        await asyncio.sleep(0.1)
        pyg.keyUp("a")
    if action == ("!rb"):
        pyg.keyDown("s")
        await asyncio.sleep(0.1)
        pyg.keyUp("s")


async def perform_game_action(action):
    if "+" in action:
        b_action = action.split("+")
        times = int(b_action[1])
        for _ in range(0, times):
            await asyncio.sleep(0.5)
            await act_on_action(b_action[0])
    else:
        await act_on_action(action)


async def check_game_action(action: str):
    keywords = ("!a", "!b", "!start", "!select", "!lb", "!rb", "!u", "!up", "!d", "!down", "!l", "!left", "!r", "!right")
    if action.startswith(keywords):
        await perform_game_action(action)


class DiscordClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.skipper = False
        self.command = ""


    # we're gonna try and get it to just edit the last message with the new screenshot as to create a more 'game-esk' screen
    async def game(self):
        
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
                    if not msg.author.name == "actes_plays_pokemon" and str(msg.content).startswith("!"):
                        await check_game_action(str(msg.content))
                await self.fastnuke()

            if msgcnt == 0:
                frame = await channel.send(file=discord.File("frame.png"))

            if msgcnt == 1:
                l_msg = all_messages[0]
                await l_msg.edit(attachments=[discord.File("frame.png")], content="Commands:\n\n!a !b !start !select !lb !rb !up !down !left !right\n\nIf you tag a + after a command followed by a number ex: 'up+5' the bot will run that command that many times!\n\n")

            #await asyncio.sleep(1)

            msgcnt = 0
            all_messages: List[discord.Message] = []

            async for x in channel.history(limit=None):
                msgcnt += 1
                all_messages.append(x)

            for msg in all_messages:
                if not msg.author.name == "actes_plays_pokemon" and str(msg.content).startswith("!"):
                    
                    await check_game_action(str(msg.content))
            
            
            await self.fastnuke()

            
        else:
            print("Failed to capture game window!")
    

    # fast nuke is for our refresh, hence we're skipping our own stuff, since well if we edit our last message we're chilling.
    async def fastnuke(self):
        print("Wiping Frame")
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
        print("Nuking channel")
        channel = self.get_channel(channel_id)
        await channel.send("Nuking the entire channel in 5")
        await asyncio.sleep(5)
        
        async for i in channel.history(limit=None):
            await i.delete()


    async def screenshot(self):
        print("Taking screenshot")
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
            print("\nFailed to capture game window!")

        
    async def on_ready(self):
        print(f"\nReady for action, running:{self.command}")
        channel = self.get_channel(channel_id)
        
        if "/game" in self.command:
            await self.game()

        if "/nuke" in self.command:
            await self.nuke()
        
        if "/ss" in self.command:
            await self.screenshot()

        if "/whoami" in self.command:
            msg = await channel.send("whoami?")
            print(msg.author.name)
            await msg.delete()

        if "/send-" in self.command:
            
            breakdown = self.command.split("-")
            breakdown.pop(0)

            messages = []

            for msg in breakdown:
                print(f"message sent:{msg}")
                messages.append(await channel.send(msg))
                

            await asyncio.sleep(5)

            for y in messages:
                await y.delete()
                
                
        print("Thread has finished, closing connection")
        
        await self.http.connector.close()
        await self.http.close()
        await self.close()


def disc_Thread(command):
    client = DiscordClient(intents=discord.Intents.default())
    client.command = command
    client.run(api_key, reconnect=False, log_handler=None)


def command_and_wait(command):
    thread = threading.Thread(target=disc_Thread,kwargs={"command": command})
    thread.start()


def game_runner():
    #print(thread_killer)
    while thread_killer:
        print("\ninit_game_loop\n")
        intents = discord.Intents.default()
        intents.message_content = True

        client = DiscordClient(intents=intents)
        client.command = "/game"
        client.run(api_key, reconnect=False, log_handler=None)

    print("game_loop_exited!")


def first_time_setup():
    disc_api_key = input("Enter bots api key:")
    chan = input("Enter channel id:")

    with open(".env", "r") as file:
        lines = file.readlines()

    with open(".env", "w") as file:
        for x, line in enumerate(lines):

            if line.startswith("DISCORD_API_TOKEN="):
                lines[x] = f"DISCORD_API_TOKEN={disc_api_key}"

            if line.startswith("CHANNEL_ID="):
                lines[x] = f"CHANNEL_ID={chan}"
    

def start_game_window() -> bool:
    try:
        subprocess.check_output("/squashfs-root/AppRun /game/pkmn_ultravhak.gba &", shell=True, text=True)
        return True
    except Exception as e:
        print(f"Failed to start subprocess:{e}")
        return False


def main():
    print("init")

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

                print(tutorial)


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
                print("Killing game thread!!")
            
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
                        print("Starting game thread!")
                    else:
                        print("Game thread already started!!")
                else:
                    print("Game appears to actually not be up!")
                    print("run /start_window and try again")

            if message == "/first":
                first_time_setup()
                
                
if __name__ == "__main__":
    print(f"Operating system is:{operating_system}")
    main()
    