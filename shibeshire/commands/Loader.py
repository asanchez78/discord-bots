from discord.ext import commands


class Loader(commands.Cog):
    """Used to manually load and unload bot modules"""
    def __init__(self, bot):
        self.bot = bot
        print("Manual Module Loader Initialized")

    @commands.command()
    async def load(self, module):
        """Load a bot module."""
        self.bot.load_extension(module)
        await self.bot.say("Loading")

    @commands.command()
    async def unload(self, module):
        """Unload a bot module."""
        self.bot.unload_extension(module)
        await self.bot.say("Unloading")

    @commands.command()
    async def reload(self, module):
        """Reload a bot module."""
        self.bot.unload_extension(module)
        self.bot.load_extension(module)
        await self.bot.say("Reloading")


def setup(bot):
    bot.add_cog(Loader(bot))
