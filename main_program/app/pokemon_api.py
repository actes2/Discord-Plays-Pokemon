import pyautogui as pyg
import discord
import asyncio
import threading
import logging
import subprocess
from dotenv import load_dotenv
import os
import sys

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
        

class DiscordClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.skipper = False
        self.command = ""

    # we're gonna try and get it to just edit the last message with the new screenshot as to create a more 'game-esk' screen
    async def game(self):
        print("Game init")
        
        self.skipper = True
        channel = self.get_channel(channel_id)
        
        
        

        gamewin = getwindowrect()
        if gamewin:

            screen = pyg.screenshot().crop([gamewin.left + 8, gamewin.top + 52, gamewin.right - 8, gamewin.bottom - 8])
            screen.save("frame.png")

            frame = await channel.send(file=discord.File("frame.png"))

            await asyncio.sleep(3)
            await self.fastnuke()
        else:
            print("Failed to capture game window!")
    

    # fast nuke is for our refresh, hence we're skipping our own stuff, since well if we edit our last message we're chilling.
    async def fastnuke(self):
        print("Wiping Frame")
        channel = self.get_channel(channel_id)
        
        messages = channel.history(limit=None, oldest_first=True)
        
        async for msg in messages:
            if channel.message_count > 1:
                await msg.delete()


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


def first_time_setup():
    chan = input("Enter channel id:")
    chan

def main():
    print("init")

    
    # thread1 = threading.Thread(target=bot_execution_thread)
    # thread1.start()
    gamer = False

    

    while True:

        if gamer:
            message_buffer.append(message)
            client = DiscordClient(intents=discord.Intents.default())
            client.run(api_key, reconnect=False)

        else:
            message = input("Message here:")
            if message == "/whoami":
                command_and_wait(message)

            if message == '/kill':
                thread_killer = False
                print("killed all threads")
            
            if message == "/ss":
                command_and_wait(message)

            if message == "/nuke":
                command_and_wait(message)

            if "/send-" in message:
                command_and_wait(message)

            if message == "/play":
                pass

            if message == "/first":
                first_time_setup()
                
                


if __name__ == "__main__":
    print(f"Operating system is:{operating_system}")
    load_dotenv()
    main()
    