import pyautogui
import discord
import asyncio
import threading

api_key = "MTIwNzA0Mzk3OTA0NTExMzkyOA.GGefJv.oW74Bj1A-EqEjwhgtv33XK84xfiWLGwj9cBkVs"
channel_id = 1206692419999891506

message_buffer = []

thread_killer = True

class DiscordClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def nuke(self):
        print("Nuking channel")
        channel = self.get_channel(channel_id)
        await channel.send("Nuking the entire channel in 5")
        await asyncio.sleep(5)
        
        async for i in channel.history(limit=None):
            await i.delete()
        


    async def on_ready(self):
        print("Ready for action")
        channel = self.get_channel(channel_id)
        #await channel.send("Ready for action!")

        # message_buffer = []
        for x in message_buffer:
            if x == "/nuke":
                await self.nuke()
                

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


    while True:
        message = input("Message here:")

        if message == 'kill':
            thread_killer = False
            print("killed all threads")
        
        if message == "/nuke":

            message_buffer.append(message)
            client = DiscordClient(intents=discord.Intents.default())
            client.run(api_key, reconnect=False)

        if "/send-" in message:

            message_buffer.append(message)
            client = DiscordClient(intents=discord.Intents.default())
            client.run(api_key, reconnect=False)
            

            



if __name__ == "__main__":
    main()
    