from discord.ext import commands


class TestCommands:
    """These are just some test commands"""
    def __init__(self, bot):
        self.bot = bot
        print("Test Commands Loaded")

    @commands.command(pass_context=True)
    async def say(self, ctx, *, something=None):
        """This command will repeat what you tell it to"""
        if something is None:
            await self.bot.say("What would you like me to say?")
        else:
            await self.bot.say("**{} said:** {}".format(str(ctx.message.author), something))
            await self.bot.delete_message(ctx.message)

    @commands.command(pass_context=True)
    async def ping(self):
        """You can ping this command.
            It will pong."""
        await self.bot.say("Pong!")


def setup(bot):
    bot.add_cog(TestCommands(bot))
