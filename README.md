# Pokemon VNC
`Twitch Plays Pokemon`-like, for any discord server

## How does it work?

This application, executes out of a `Docker` container, which creates an internal VNC server which we screenshot images from a self-contained emulator and pokemon rom.

These screenshots are then sent to a Discord server via a discord-bot with a provisioned channel dedicated to the bot.

Additionally, users in the channel established for the discord bot, can send commands over to interact with the bot itself.

## Commands
Users can interact with the game by sending one of the following inputs into the chat, after 5 seconds the bot will ingest all of the commands and execute them in accordance.

```
!a - A
!b - B

!l - Left (You can also type the full word !left)
!u - Up (You can also type the full word !up)
!r - Right (You can also type the full word !right)
!d - Down (You can also type the full word !down)

!start - Start
!select - Select

!lb - Left Bumper
!rb - Right Bumper
```

You may also chain multiple inputs into a command, for instance to move right 5 times, you'd type: `!r+5`
>Maximum allowed is 10 chained inputs at a time.

## Discord Bot setup
For setting up the discord bot, you'll need to just provision a dedicated bot with the following permissions:
  * read, write channel access
  * read, write user content
  * ability to edit its own messages
  * ability to delete user messages (for clean-up)
  * ability to delete its own messages

## Deployment

Make sure you have `Docker` installed you can get it [here](https://docs.docker.com/engine/install/)

After setting up the discord bot, add the bot to your server, and give it a specific channel
>Note renaming the bot may mess it up

clone this repository to whatever we'll be hosting the bot via docker on, and add to the `/main_program/app/` directory a `.env` file

Your `.env` file should look like this:
```
API_KEY=<Your API Key>
BOT_NAME=<Your Bot Name>
CHANNEL_ID=<Your channel ID for the Bot>
```

Once this has been setup, go ahead and run a command-line in the `/main_program` directory and execute the command:
`docker build -t pokemon_vnc`

Once the build has been completed, you can then just run the docker container with:
`docker run -d pokemon_vnc`

If everything was established properly you should now have a discord bot playing my included version of a romhack I found online!

You will need to add the bot to a `DEDICATED` Discord channel - if you do not give it a *dedicated channel it will **delete** all chat logs in the channel you put it in*
