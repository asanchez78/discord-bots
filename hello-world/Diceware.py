import random
import discord
from discord.ext import commands

client = discord.Client()


class Diceware:
    """Used to generate Diceware pass phrases."""
    def __init__(self, bot):
        self.bot = bot
        self.__word_number = ''
        self.__word_list = []
        self.__word = ''
        print("Diceware Loaded")

    @commands.command(pass_context=True)
    async def wordlist(self, ctx, num_of_words=None):
        """- This command will return a number of words specified in the command"""
        if num_of_words is None:
            await self.bot.say('How many words would you like to generate?')
        else:
            num_of_words = int(num_of_words)
            # derive x number of words as specified in the bot command
            for x in range(num_of_words):
                # words in the list are numbered with four digit numbers. roll four
                # six-sided dice
                for y in range(4):
                    die = random.randint(1, 6)
                    # concatenate each die roll to form a four digit number
                    self.__word_number = self.__word_number + str(die)
                # call get_word function to retrieve the word corresponding to the number generated
                self.__get_word(self.__word_number)
                # reset the word number
                self.__word_number = ''
                # append word to list
                self.__word_list.append(self.__word)
            # send a message to the channel with the word list
            await self.bot.say('{}, your words are {}'.format(str(ctx.message.author), self.__word_list))
            # reset the word list
            self.__word_list = []

    def __get_word(self, word_num):
        """Takes a four digit number as input. Returns the word represented by the number as a string."""

        word_list_file = open('eff_short_wordlist_2_0.txt', 'r')
        # read each line until a match is found for the word number
        for line in word_list_file:
            if word_num in line:
                self.__word = line
        # split the string and remove the number returning only the word
        self.__word = self.__word.split()
        self.__word = self.__word[1]
        word_list_file.close()
        return self.__word


def setup(bot):
    bot.add_cog(Diceware(bot))
