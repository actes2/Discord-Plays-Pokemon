import pyautogui as pyg
import discord
import asyncio
import threading
import logging
import subprocess
import sys

logger = logging.getLogger()

api_key = "MTIwNzA0Mzk3OTA0NTExMzkyOA.GGefJv.oW74Bj1A-EqEjwhgtv33XK84xfiWLGwj9cBkVs"
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
            return [gamewin.left + 8, gamewin.top + 52, gamewin.right - 8, gamewin.bottom - 8]
        except:
            return None
    else:
        try:
            output = subprocess.check_output("wmctrl -lG | grep 'mGBA'", shell=True, text=True).split()
            return [int(output[2]) + 8, int(output[3]) + 52, int(output[4]) - 8, int(output[5]) - 8]
        except:
            return None
        

class DiscordClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.skipper = False

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
            if not msg.author.name == "actes_plays_pokemon":
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

        gamewin = pyg.getWindowsWithTitle("mGBA")[0]
        screen = pyg.screenshot().crop([gamewin.left + 8, gamewin.top + 52, gamewin.right - 8, gamewin.bottom - 8])
        screen.save("frame.png")

        frame = await channel.send(file=discord.File("frame.png"))
        await asyncio.sleep(3)
        await frame.delete()

        
    async def on_ready(self):
        print("Ready for action")
        channel = self.get_channel(channel_id)
        #await channel.send("Ready for action!")

        # message_buffer = []
        for x in message_buffer:
            if x == "/game":
                await self.game()

            if x == "/nuke":
                await self.nuke()
            
            if x == "/ss":
                await self.screenshot()

            if "/send-" in x:
                
                breakdown = x.split("-")
                breakdown.pop(0)

                messages = []

                for msg in breakdown:
                    print(f"message sent:{msg}")
                    messages.append(await channel.send(msg))

                await asyncio.sleep(5)

                for y in messages:
                    await y.delete()
                

        print("Clearing buffer and closing connection")
        

        message_buffer.clear()
        
        await self.close()
        await self.http.close()
        await self.http.connector.close()

        loop = asyncio.get_event_loop()
        loop.stop()
        loop.close()        
        
        
        
            

# @client.event
# async def on_ready():
#     print("Ready for action")
#     channel = client.get_channel(channel_id)
#     #await channel.send("Ready for action!")

#     # message_buffer = []
#     for x in message_buffer:
#         print(f"message sent and popped off the buffer:{x}")
#         await channel.send(x)
#     await client.close()


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
            
            if message == "/game":
                gamer = True

            if message == 'kill':
                thread_killer = False
                print("killed all threads")
            
            if message == "/ss":
                message_buffer.append(message)
                client = DiscordClient(intents=discord.Intents.default())
                client.run(api_key, reconnect=False)


            if message == "/nuke":
                message_buffer.append(message)
                client = DiscordClient(intents=discord.Intents.default())
                client.run(api_key, reconnect=False)

            if "/send-" in message:

                message_buffer.append(message)
                client = DiscordClient(intents=discord.Intents.default())

                client.run(api_key, reconnect=False)
                                

                
                
            

            



if __name__ == "__main__":
    print(f"Operating system is:{operating_system}")

    main()
    