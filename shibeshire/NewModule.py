from discord.ext import commands


class NewCommands:

    def __init__(self, bot):
        self.bot = bot
        print("New Commands Loaded")

    @commands.command(pass_context=True)
    async def syn(self):
        """You can send a syn packet.
            It will ack."""
        await self.bot.say("ack!")


def setup(bot):
    bot.add_cog(NewCommands(bot))
