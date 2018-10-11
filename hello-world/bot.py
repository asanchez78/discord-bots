from discord.ext import commands

bot = commands.Bot(description="This is my hello world bot", command_prefix="/hw ")
bot_token = ''

@bot.event
async def on_ready():
    bot.load_extension("Loader")
    bot.load_extension("TestCommands")
    bot.load_extension("Diceware")


bot.run(bot_token)
