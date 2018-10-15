import random
import argparse


def main():
    parser = argparse.ArgumentParser(description='Gives a word list')
    parser.add_argument('-w', '--words', help='Number of words', required=False)
    parser.add_argument('-id', '--wordid', help='The numbers manually rolled with a d6', required=False)
    args = parser.parse_args()

    word_list = 'eff_short_wordlist_2_0.txt'

    word_id_length = 4

    diceware = Diceware(word_list, word_id_length)

    if args.wordid:
        word = diceware.get_single_word(args.wordid)
        print('The word for {} is {}'.format(args.wordid, word))
    else:
        number = random.randint(0, 100)
        diceware.generate_wordlist(args.words)
        wordlist = diceware.get_word_list()
        print('Your {} words are "{}" and your random number is {}'.format(args.words, wordlist, number))


class Diceware:
    """Used to generate Diceware pass phrases."""
    def __init__(self, words_file, word_id_length):
        self.__word_list = []
        self.__word = ''
        self.__word_list_file = words_file
        self.__word_id_length = word_id_length

    def generate_wordlist(self, num_of_words):
        """- This method will return the number of words passed"""
        num_of_words = int(num_of_words)
        word_id = ''
        # derive x number of words
        for x in range(num_of_words):
            # words in the list are numbered. roll six-sided dice to get the word number
            for y in range(self.__word_id_length):
                die_roll = random.randint(1, 6)
                # concatenate each die roll to form a word id
                word_id = word_id + str(die_roll)
            # call lookup_word function to retrieve the word corresponding to the word id generated
            self.__lookup_word(word_id)
            # reset the word id number
            word_id = ''
            # append word to list
            self.__word_list.append(self.__word)

    def get_word_list(self):
        words = ''
        for word in self.__word_list:
            words += word + ' '

        return words.rstrip()

    def get_single_word(self, word_id):
        self.__lookup_word(word_id)
        return self.__word

    def __lookup_word(self, word_num):
        """Takes an integer as input. Returns the word represented by the number from the word list."""

        word_list_file = open(self.__word_list_file, 'r')
        # read each line until a match is found for the word number
        for line in word_list_file:
            if word_num in line:
                self.__word = line
        # split the string and remove the number returning only the word
        self.__word = self.__word.split()
        self.__word = self.__word[1]
        word_list_file.close()


if __name__ == '__main__':
    main()
