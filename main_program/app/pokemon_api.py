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
channel_id = 1206692419999891506

message_buffer = []

thread_killer = True


if sys.platform.startswith("win"):
    operating_system = "windows"
else:
    operating_system = "linux"
        

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
            return [int(output[2]) + 11, int(output[3]) + 76, int(output[4]) - 11, int(output[5]) - 11]
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
    print("Check gmae action is hit")
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
        print("Game init")
        
        channel = self.get_channel(channel_id)
        msgcnt = 0
        all_messages: List[discord.Message] = []

        async for x in channel.history(limit=None):
            msgcnt += 1
            all_messages.append(x)

        print("got channel")
        gamewin = getwindowrect()
        if gamewin:
            print("Got game window")
            screen = pyg.screenshot().crop(gamewin)
            screen.save("frame.png")
            print("Made it past our screenshot save?!?!")

            print(f"number of messages before we figure out wtf to do: {msgcnt}")
            if msgcnt > 1:
                for msg in all_messages:
                    print(f"{msg.content}\n")
                    if not msg.author.name == "actes_plays_pokemon" and str(msg.content).startswith("!"):
                        print("Non bot author found!!!!")

                        await check_game_action(str(msg.content))
                await self.fastnuke()
            if msgcnt == 0:
                frame = await channel.send(file=discord.File("frame.png"))
            if msgcnt == 1:
                l_msg = all_messages[0]
                print(f"attachments: {type(l_msg.attachments[0])}")
                await l_msg.edit(attachments=[discord.File("frame.png")], content="Commands:\n\n!a !b !start !select !lb !rb !up !down !left !right\n\nIf you tag a + after a command followed by a number ex: 'up+5' the bot will run that command that many times!\n\n")

                
                #await l_msg.edit(embed=discord.File("frame.png"))
                
                #frame = await channel.last_message.edit(attachments=discord.File("frame.png"))
            print("Made it through edit or make new message block")

            await asyncio.sleep(3)

            msgcnt = 0
            all_messages: List[discord.Message] = []

            async for x in channel.history(limit=None):
                msgcnt += 1
                all_messages.append(x)

            print(f"\n{all_messages} the length is: {len(all_messages)}")
            if len(all_messages) > 1:
                print(all_messages[1].content)

            for msg in all_messages:
                print(f"{msg.content}\n")
                if not msg.author.name == "actes_plays_pokemon" and str(msg.content).startswith("!"):
                    print("Non bot author found!!!!")
                    await check_game_action(str(msg.content))
            
            print("made it to fast nuke")
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

        # messages = await channel.history(limit=None, oldest_first=True)
        
        # async for msg in messages:
        #     if channel.message_count > 1 and not msg.author.name == "actes_plays_pokemon":
        #         await msg.delete()


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
            screen = pyg.screenshot().crop(gamewin)
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
    print(thread_killer)
    while thread_killer:
        print("\ninit_game_loop\n")
        intents = discord.Intents.default()
        intents.message_content = True

        client = DiscordClient(intents=intents)
        client.command = "/game"
        client.run(api_key, reconnect=False, log_handler=None)

    print("game_loop_exited!")



def first_time_setup():
    chan = input("Enter channel id:")
    chan

def main():
    print("init")

    
    # thread1 = threading.Thread(target=bot_execution_thread)
    # thread1.start()
    gamer = False
    thread_killer = False
    

    while True:

        if gamer:
            message_buffer.append(message)
            client = DiscordClient(intents=discord.Intents.default())
            client.run(api_key, reconnect=False)

        else:
            message = input("Message here:")

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

            if message == "/game":
                if not thread_killer:
                    thread_killer = True

                    thread = threading.Thread(target=game_runner)
                    thread.start()
                    print("Starting game thread!")
                else:
                    print("Game thread already started!!")

            if message == "/first":
                first_time_setup()
                
                


if __name__ == "__main__":
    print(f"Operating system is:{operating_system}")
    main()
    