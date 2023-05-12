import discord
from discord.ext import commands

class MusicBot(commands.Bot):

    def __init__(self):
        super().__init__(command_prefix="!")
        self.voice_clients = {}

    @commands.command()
    async def play(self, ctx, *, query):
        # Check if the user is in a voice channel
        if ctx.author.voice is None:
            await ctx.send("You must be in a voice channel to use this command.")
            return

        # Get the user's current voice channel
        voice_channel = ctx.author.voice.channel

        # Find the first song that matches the query
        song = await self.find_song(query)

        # If no song was found, send an error message
        if song is None:
            await ctx.send("No song was found for that query.")
            return

        # Create a new voice client and connect it to the user's voice channel
        voice_client = await self.join_voice_channel(voice_channel)

        # Play the song
        await voice_client.play(song)

    @commands.command()
    async def pause(self, ctx):
        # Check if the bot is currently playing music
        if not self.voice_clients[ctx.guild.id]:
            await ctx.send("I am not currently playing music.")
            return

        # Pause the current song
        await self.voice_clients[ctx.guild.id].pause()

    @commands.command()
    async def resume(self, ctx):
        # Check if the bot is currently playing music
        if not self.voice_clients[ctx.guild.id]:
            await ctx.send("I am not currently playing music.")
            return

        # Resume the current song
        await self.voice_clients[ctx.guild.id].resume()

    @commands.command()
    async def stop(self, ctx):
        # Check if the bot is currently playing music
        if not self.voice_clients[ctx.guild.id]:
            await ctx.send("I am not currently playing music.")
            return

        # Stop the current song and disconnect the voice client
        await self.voice_clients[ctx.guild.id].stop()
        await self.voice_clients[ctx.guild.id].disconnect()
        del self.voice_clients[ctx.guild.id]

    async def find_song(self, query):
        # Search for the song on YouTube
        search_results = await self.session.get("https://www.googleapis.com/youtube/v3/search?part=snippet&q={}".format(query))
        search_results = search_results.json()

        # If no results were found, return None
        if not search_results["items"]:
            return None

        # Get the first result
        result = search_results["items"][0]

        # Get the video ID
        video_id = result["id"]["videoId"]

        # Get the song URL
        song_url = "https://www.youtube.com/watch?v={}".format(video_id)

        return song_url


if __name__ == "__main__":
    # Get the bot token from the environment variable
    BOT_TOKEN = os.environ["BOT_TOKEN"]

    # Create the bot
    bot = MusicBot()

    # Run the bot
    bot.run(BOT_TOKEN)
