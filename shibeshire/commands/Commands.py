from discord.ext import commands
import random
import asyncio
from datetime import datetime
from models import ynab_bills
from models.diceware import Diceware
import config


class Commands(commands.Cog):
    """Utility commands"""
    def __init__(self, bot):
        self.bot = bot
        print("Commands Loaded")

    @commands.command()
    @asyncio.coroutine
    def bills(self, ctx, start_date=None):
        """Lists bills due within two weeks of the entered date."""
        if start_date is None:
            yield from ctx.send("I need to know the date for the bills you want (ex: 10-12-2018).")
        else:
            try:
                # take the start date and get the date 13 days out
                dates = ynab_bills.get_dates(first_date=start_date)
                start_date = dates[0]
                end_date = dates[1]
                print('Getting bills beginning from ' + str(start_date) + ' to ' + str(end_date))
                # get the list of bills
                message = ynab_bills.get_bills(start_date, end_date)
                yield from ctx.send(message)
            except ValueError as err:
                print(err)
                yield from ctx.send("Invalid date format (ex: 10-12-2018).")

    @commands.command(pass_context=True)
    @asyncio.coroutine
    def wordlist(self, ctx, num_of_words=None):
        word_file = 'models/eff_short_wordlist_2_0.txt'
        """Generates a list of words using the diceware method"""
        if num_of_words is None:
            yield from ctx.send('How many words would you like to generate?')
        else:
            num_of_words = int(num_of_words)
            word_id_length = 4

            words = Diceware(word_file, word_id_length)

            number = random.randint(0, 100)
            words.generate_wordlist(num_of_words)
            wordlist = words.get_word_list()
            yield from ctx.send('{}, your {} words are "{}" and your random number is {}'
                                .format(str(ctx.message.author), num_of_words, wordlist, number))


def setup(bot):
    bot.add_cog(Commands(bot))
