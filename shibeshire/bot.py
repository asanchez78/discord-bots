from discord.ext import commands
import config

bot = commands.Bot(description="This is my hello world bot", command_prefix="/")


@bot.event
async def on_ready():
    bot.load_extension("commands.Loader")
    bot.load_extension("commands.Commands")
    bot.load_extension("commands.Diceware")


bot.run(config.bot_token)
