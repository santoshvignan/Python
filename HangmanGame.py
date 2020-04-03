import random
import sys

#Picking words from Dictionary
word = open("/usr/share/dict/words","r")

class Verify(object):
    def __init__(self,guess_letter,chosen_word,Word,chance,previous_guess):
        self.guess_letter = guess_letter
        self.chosen_word = chosen_word
        self.Word = Word
        self.chance = chance
        self.previous_guess = previous_guess

    def verifyword(self):

        while self.chance != 0:
            #Make the user to choose a letter only once
            if self.guess_letter == self.previous_guess:
                print (self.guess_letter + " has already been chosen. Choose a different letter")
                self.wordguess()

            #The guessed letter is looked in the random word chosen from the list. After it is found, we find the index of
            #that guessed letter in the chosen word and replace that letter at the same position in word.
            if self.guess_letter in self.chosen_word:
                print (self.guess_letter + " is present in the word")
                self.previous_guess = self.guess_letter
                repeat_count = self.chosen_word.count(self.guess_letter)
                count = 0
                if repeat_count != 0:

                    for i in range(0,len(self.chosen_word)):
                        if count < repeat_count and self.chosen_word[i] == self.guess_letter:

                            self.Word[self.chosen_word.index(self.guess_letter,
                                                self.chosen_word.index(self.guess_letter) + count)] = self.guess_letter
                            count = count + 1
                else:
                    self.Word[self.chosen_word.index(self.guess_letter)] = self.guess_letter

                if "".join(self.Word) == self.chosen_word:
                    print ("Congratulations. You have won. The word is " + "".join(self.Word))
                    sys.exit()
                else:
                    print ("You have " + str(self.chance) + " chances remaining. Word is " +
                           "".join(self.Word))
                    self.wordguess()

            else:
                print (self.guess_letter + " is not present in the word")
                self.previous_guess = self.guess_letter
                self.chance = self.chance - 1

                if self.chance == 0:
                    print ("Game Over")
                    print ("The word chosen was ", self.chosen_word)
                    sys.exit()
                else:
                    print("You have " + str(self.chance) + " chances remaining. Word is " +
                          "".join(self.Word))
                    self.wordguess()


    def wordguess(self):

        print ("Your previous guess is " + self.previous_guess)
        user_guess = input("What is your next guess: ")
        while user_guess.isdigit():
            print ("Please enter an alphabet")
            user_guess = input("What is your guess: ")

        next_guessed_letter = Verify(user_guess.upper(),self.chosen_word,self.Word,self.chance,self.previous_guess)
        next_guessed_letter.verifyword()


if __name__ == '__main__':
    print ("Welcome to the Hangman game. \m/")
    chances = int(input("Enter a number between 1 and 25: "))
    while chances < 0 or chances > 25:
        chances = int(input("Enter a number between 1 and 25: "))
    len_word = int(input("What is the size of the word you want to guess? "))
    print ("Selecting a word.....")
    len_word_list = []
    for i in word.read().splitlines():
        if len(i) == len_word:
            len_word_list.append(i)
    random_word = random.choice(len_word_list)
    previous_guess = ""
    print ("Your previous guess was: " + previous_guess)
    Word = []
    for i in range(0,len_word):
        Word.append("_")
    print ("The word is " + "".join(Word))
    user_guess = input("What is your guess: ")
    while user_guess.isdigit():
        print ("Please enter an alphabet")
        user_guess = input("What is your guess: ")
    guessed_letter = Verify(user_guess.upper(),random_word,Word,chances,previous_guess)
    guessed_letter.verifyword()
