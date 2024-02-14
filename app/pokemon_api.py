import pyautogui
import discord
import asyncio
import threading

api_key = "MTIwNzA0Mzk3OTA0NTExMzkyOA.GGefJv.oW74Bj1A-EqEjwhgtv33XK84xfiWLGwj9cBkVs"
channel_id = "1206692419999891506"

thread_killer = True
last_command = ""

class discordClient(discord.Client):
    async def on_ready(self):
        print("live and kicking")
    
    async def send_message(self, message_to_send):
        channel = self.get_channel(channel_id)
        await channel.send(message_to_send)

bot = discordClient(intents=None)

def bot_thread():
    
    bot.run(api_key)


def main():
    print("init")

    thread = threading.Thread(target=bot_thread)
    thread.start()
    while True:
        pass
    
    exit()



if __name__ == "__main__":
    main()