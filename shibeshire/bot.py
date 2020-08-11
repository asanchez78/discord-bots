from discord.ext import commands
import datetime
import config

bot = commands.Bot(description="This is my hello world bot", command_prefix="/")


@bot.event
async def on_ready():
    bot.load_extension("commands.Commands")
    bot.load_extension("commands.Loader")

print('Initializing bot ' + str(datetime.datetime.now()))
bot.run(config.bot_token)
