# Imported Libraries #
import discord
import requests
import asyncio
import yt_dlp as youtube_dl

# Reassignment Keys #
intents = discord.Intents().all()
client = discord.Client(intents=intents)

# Blank Client Dictionary #
voice_clients = {}

# Music Options #
yt_dl_opts = {'format': 'bestaudio/best', 'noplaylist': 'True'}
ytdl = youtube_dl.YoutubeDL(yt_dl_opts)

ffmpeg_options = {'options': '-vn'}


# Functions #
# Gets random insult from evilinsult api #
def get_quote():
    response = requests.get("https://evilinsult.com/generate_insult.php?")
    quote = response.text
    return quote


# Word Banks for Message Actions - Keep them lowercase #
typing = ["fast", "speed", "typing", 'keyboard', "switches", "quick", "type"]

banned = ["fuck", "fucked", "fucker", "shitter", "shit", "cunt", "damn", "ass", "pussy", "kys",
          "nig", "nigga", "nigger", ]
Max = ["gay", "max", "homo", "gay", "homo"]

greetings = ["Hi", "hi", "hello", "Hello", "whats good", "whats up", "wya"]

doug = ["cock", "meat", "penis", "hard", "dick"]


# Client Events #
@client.event
async def on_ready():
    print("Holy freakin' smokes I'm in his butt and im logged in to Discord as {0.user}!".format(client))
    channel = client.get_channel(1102412567659425835)
    await channel.send("Holy freakin' smokes I'm in this butt and im logged in to Discord as {0.user}! Get ready for "
                       "me to spread your wonder holes. Especially you, Brandon.".format(client))


@client.event
async def on_message(message):
    # Shortening Directories #
    user = message.author
    # Checks that the message wasn't sent by the bot #
    if message.author == client.user:
        return
    # If a user mentions the bot #
    if client.user.mentioned_in(message):
        await message.channel.send("What's good you shrimp boy?")
    # If a user talks about Thomas #
    if any(word in message.content.lower() for word in doug):
        await message.channel.send("After closely inspecting his meat hammer, I have deduced that Doug's scepter is "
                                   "approximately "
                                   "14.32 inches hard.")
    # Creates a random insult #
    if message.content.lower().startswith("$insult"):
        quote = get_quote()
        await message.channel.send(quote)
    # Banned word action #
    if any(word in message.content.lower() for word in banned):
        get_quote()
        s = get_quote()
        await message.channel.send(f"{user.mention} {s} It is so important that you understand that this kind of "
                                   f"language is absolutely NOT allowed "
                                   f"in my discord server. Try that shit again and you will be permanently removed.")
    # Brags about Thomas' typing speed#
    if any(word in message.content.lower() for word in typing):
        await message.channel.send(f"{user.mention} Have you seen how fast Doug can type on his Q5 though? Check this "
                                   f"out: https://data.typeracer.com/misc/badge?user=slylar45")

    # Mentions Max's sexuality if something similar is discussed #
    if any(word in message.content.lower() for word in Max):
        await message.channel.send("Ive often been asked about Max's sexuality. You don't need access to the entire "
                                   "library of the internet to see that mountain "
                                   "standing in front of you. But I do have that kind of access, and I can confirm "
                                   "that Max is in fact, gay.")
    # Music Player #
    if message.content.lower().startswith("play"):

        try:
            voice_client = await message.author.voice.channel.connect()
            voice_clients[voice_client.guild.id] = voice_client
        except:
            await message.channel.send("Error playing file.")

        try:
            url = message.content.split()[1]

            loop = asyncio.get_event_loop()
            data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=False))

            song = data['url']
            player = discord.FFmpegPCMAudio(song, **ffmpeg_options)

            voice_clients[message.guild.id].play(player)
        except Exception as err:
            await message.channel.send(f"{err}.")

    if message.content.lower().startswith("pause"):
        try:
            voice_clients[message.guild.id].pause()
        except Exception as err:
            print(err)

    # This resumes the current song playing if it's been paused
    if message.content.lower().startswith("resume"):
        try:
            voice_clients[message.guild.id].resume()
        except Exception as err:
            print(err)

    # This stops the current playing song
    if message.content.lower().startswith("stop"):
        try:
            voice_clients[message.guild.id].stop()
            await voice_clients[message.guild.id].disconnect()
        except Exception as err:
            print(err)


# Client Key - DO NOT TOUCH OR EDIT BELOW THIS LINE - #
client.run('MTEwMjQxMzE4OTE2MzAxMjA5Ng.GG2F9K.Lv24TcVJ8I-WBIbgyrA2SipmMUaOJq66TBbjG0')
