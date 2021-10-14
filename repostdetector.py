import os
import discord
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL1 = os.getenv("CHANNEL1")
CHANNEL2 = os.getenv("CHANNEL2")

client = discord.Client()

@client.event
async def on_ready():
    print(f"{client.user} has connected to Discord!")

@client.event
async def on_disconnect():
    print(f"{client.user} has disconnected from Discord!")

@client.event
async def on_message(message):
    # Ignore messages from the bot itself
    if message.author == client.user:
        return

    # Shutdown bot with command
    if message.content.startswith("!killrpb"):
        await client.logout()

    # Only check for reposted Twitter URLs
    if "https://twitter.com/" in message.content:
        # Save channel ID
        channelID = message.channel.id

        if channelID == int(CHANNEL1) or channelID == int(CHANNEL2):
            print("Looking for message: " + message.content)
            activeChannel = client.get_channel(channelID)

            # Get the most recent messages and put them into a list
            messageLog = await activeChannel.history(limit = 50, oldest_first = False).flatten()

            # Remove the current message to avoid counting it as a repost
            messageLog.pop(0)
            # print(messageLog)

            for originalMsg in messageLog:
                if message.content in originalMsg.content:
                    print("Found repost!")
                    await message.add_reaction("♻")
                    await activeChannel.send("Repost detected! Original post here: " + originalMsg.jump_url, delete_after = 10)

client.run(TOKEN)