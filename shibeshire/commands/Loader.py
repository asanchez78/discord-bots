from discord.ext import commands
import asyncio


class Loader(commands.Cog):
    """Used to manually load and unload bot modules"""
    def __init__(self, bot):
        self.bot = bot
        print("Manual Module Loader Initialized")

    @commands.command()
    @asyncio.coroutine
    def load(self, ctx, module):
        """Load a bot module."""
        self.bot.load_extension(module)
        yield from ctx.send("Loading")

    @commands.command()
    @asyncio.coroutine
    def unload(self, ctx, module):
        """Unload a bot module."""
        print("Module = " + module)
        self.bot.unload_extension(module)
        yield from ctx.send("Unloading")

    @commands.command()
    @asyncio.coroutine
    def reload(self, ctx, module):
        """Reload a bot module."""
        self.bot.unload_extension(module)
        self.bot.load_extension(module)
        yield from ctx.send("Reloading")


def setup(bot):
    bot.add_cog(Loader(bot))
