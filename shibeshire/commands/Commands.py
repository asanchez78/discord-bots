from discord.ext import commands
from models import bills


# import discord


class Commands:
    """Utility commands"""
    def __init__(self, bot):
        self.bot = bot
        print("Commands Loaded")

    # @commands.command(pass_context=True)
    # async def say(self, ctx, *, something=None):
    #     """This command will repeat what you tell it to"""
    #
    #     if something is None:
    #         await self.bot.say("What would you like me to say?")
    #     else:
    #         dest_channel = discord.utils.get(ctx.message.server.channels, name="testing",
    #                                          type=discord.ChannelType.text)
    #         print(dest_channel.id)
    #
    #         await self.bot.say("**{} said:** {}".format(str(ctx.message.author), something))
    #         await self.bot.send_message(discord.Object(id=dest_channel.id), something)
    #         await self.bot.delete_message(ctx.message)

    @commands.command(pass_context=True)
    async def bills(self, ctx, start_date=None, end_date=None):
        """Lists bills due between two dates supplied. (ex: 2018-09-1 2018-09-14)"""
        if start_date is None or end_date is None:
            await self.bot.say("I need to know the dates for the bills you want (ex: 2018-09-1 2018-09-14). ")
        start_date = bills.format_date(start_date)
        end_date = bills.format_date(end_date)
        message = bills.bills(start_date, end_date)
        await self.bot.say(message)


def setup(bot):
    bot.add_cog(Commands(bot))
