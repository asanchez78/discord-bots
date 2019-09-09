from discord.ext import commands
import random
from models import bills
from models.diceware import Diceware
import asyncio


# import discord


class Commands(commands.Cog):
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

    @commands.command()
    async def bills(self, ctx, start_date=None):
        """Lists bills due within two weeks of the entered date."""
        if start_date is None:
            await ctx.send("I need to know the date for the bills you want (ex: 10-12-2018).")

        dates = bills.get_dates(start_date)
        start_date = dates[0]
        end_date = dates[1]
        print('Getting bills beginning from ' + start_date + ' to ' + end_date)
        message = bills.bills(start_date, end_date)
        await ctx.send(message)

    @commands.command()
    async def wordlist(self, ctx, num_of_words=None):
        word_file = 'models/eff_short_wordlist_2_0.txt'
        """Generates a list of words using the diceware method"""
        if num_of_words is None:
            await ctx.send('How many words would you like to generate?')
        else:
            num_of_words = int(num_of_words)
            word_id_length = 4

            words = Diceware(word_file, word_id_length)

            number = random.randint(0, 100)
            words.generate_wordlist(num_of_words)
            wordlist = words.get_word_list()
            await ctx.send('{}, your {} words are "{}" and your random number is {}'
                               .format(str(ctx.message.author), num_of_words, wordlist, number))


def setup(bot):
    bot.add_cog(Commands(bot))
