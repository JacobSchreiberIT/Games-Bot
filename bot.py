import discord
import responses
import os
import random
from dotenv import load_dotenv
from english_words import get_english_words_set

#load enviroment variables, these variables are used to store sensitive data
load_dotenv()

#rock paper scissors containers
RPS_dict = dict()
RPS_list = ["rock", "paper", "scissors"]

#Hangman variables and containers and wordsets
web2lowerset = get_english_words_set(['web2'], lower=True)
gaming_words = list()
with open('hangman_gaming_words.txt', 'r') as file:
    for line in file:
        gaming_words.append(line.strip('\n'))
guesses = 5
play_hangman = False
used_letters = set()
letters_list = list()
output_list = list()

def run_discord_bot():
    intents = discord.Intents.default()
    intents.message_content = True
    #sets client to my Client() object
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        print(f'{client.user} is now running!')

    @client.event
    async def on_message(message):
        #so bot does not respond to itself
        if message.author == client.user:
            return

        #gather info about user
        username = str(message.author)
        user_message = str(message.content).lower()
        channel = str(message.channel)

        print(f'{username} said: "{user_message}" ({channel})')

        await Games(message, user_message, username)

    client.run(os.getenv("token"))


async def Games(message, user_message, username):
    if username not in RPS_dict:
        RPS_dict[username] = 0
        RPS_dict[username + "bot"] = 0

    try:
        response = responses.get_response(user_message)

        global play_hangman
        global guesses
        global letters_list
        global output_list
        global used_letters

        if play_hangman:
            if len(user_message) != 1:
                await message.channel.send("Please only enter a single letter")
            elif user_message in used_letters:
                await message.channel.send("You already guessed that letter")
            else:
                found = False
                used_letters.add(user_message)
                for i in range(len(letters_list)):
                    if user_message == letters_list[i]:
                        output_list[i] = user_message
                        found = True
                if output_list == letters_list:
                    temp_word = ""
                    for letter in letters_list:
                        temp_word += letter
                    await message.channel.send(f'Correct, the word was: {temp_word}')
                    play_hangman = False
                    guesses = 5
                    used_letters = set()
                    letters_list = list()
                    output_list = list()
                    return
                    
                if found == False:
                    guesses -= 1

                if guesses == 0:
                    temp_word = ""
                    for letter in letters_list:
                        temp_word += letter
                    await message.channel.send(f'Out of guesses the word was: {temp_word}')
                    play_hangman = False
                    guesses = 5
                    used_letters = set()
                    letters_list = list()
                    output_list = list()
                else:
                    temp_word = ""
                    for letter in output_list:
                        temp_word += letter + " "
                    await message.channel.send(f'guesses remaining: {guesses} \nUsed letters: {used_letters}\nWord: {temp_word}')

        #Play rock paper scissors
        elif response == "RPS":
            #return rock, paper or scissors
            computer_choice = RPS_list[random.randint(0,2)]
            if user_message== computer_choice:
                await message.channel.send(f'Computer choice: {computer_choice}\nIt is a Tie!\nScore: {username} {RPS_dict[username]} | Computer {RPS_dict[username + "bot"]}')
            elif user_message == "rock" and computer_choice == "scissors":
                RPS_dict[username] += 1
                await message.channel.send(f'Computer choice: {computer_choice}\n{username} Wins!\nScore: {username} {RPS_dict[username]} | Computer {RPS_dict[username + "bot"]}')
            elif user_message == "rock" and computer_choice == "paper":
                RPS_dict[username + "bot"] += 1
                await message.channel.send(f'Computer choice: {computer_choice}\nThe computer Wins!\nScore: {username} {RPS_dict[username]} | Computer {RPS_dict[username + "bot"]}')
            elif user_message == "paper" and computer_choice == "rock":
                RPS_dict[username] += 1
                await message.channel.send(f'Computer choice: {computer_choice}\n{username} Wins!\nScore: {username} {RPS_dict[username]} | Computer {RPS_dict[username + "bot"]}')
            elif user_message == "paper" and computer_choice == "scissors":
                RPS_dict[username + "bot"] += 1
                await message.channel.send(f'Computer choice: {computer_choice}\nThe computer Wins!\nScore: {username} {RPS_dict[username]} | Computer {RPS_dict[username + "bot"]}')
            elif user_message == "scissors" and computer_choice == "paper":
                RPS_dict[username] += 1
                await message.channel.send(f'Computer choice: {computer_choice}\n{username} Wins!\nScore: {username} {RPS_dict[username]} | Computer {RPS_dict[username + "bot"]}')
            elif user_message == "scissors" and computer_choice == "rock":
                RPS_dict[username + "bot"] += 1
                await message.channel.send(f'Computer choice: {computer_choice}\nThe computer Wins!\nScore: {username} {RPS_dict[username]} | Computer {RPS_dict[username + "bot"]}')
        
        elif response == "HANGMAN" or response == "GAMING HANGMAN":
            play_hangman = True
            if response == "HANGMAN":
                word = random.choice(tuple(web2lowerset))
            else:
                word = gaming_words[random.randint(0,len(gaming_words) - 1)]
            print("The random chosen word is: ", word)
            len_letters = ""
            for letter in word:
                if letter == " ":
                    len_letters += " "
                else:
                    len_letters += "\_ "
            for letter in word:
                letters_list.append(letter)
                if letter == " ":
                    output_list.append(" ")
                else:
                    output_list.append("\_")
            await message.channel.send(f'guesses remaining: {guesses}\n\nWord: {len_letters}')

        elif user_message == "!help":
            await message.channel.send(response)
        else:
            await message.channel.send(response)
    except Exception as e:
        print(e)