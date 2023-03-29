import discord
import responses
import os
import random
from dotenv import load_dotenv
from english_words import get_english_words_set

#load enviroment variables, these variables are used to store sensitive data
load_dotenv()

#set of words
web2lowerset = get_english_words_set(['web2'], lower=True)

#rock paper scissors containers
RPS_dict = dict()
RPS_list = ["rock", "paper", "scissors"]

#Hangman variables and containers
guesses = 5
used_letters = set()
booly = False

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
        user_message = str(message.content)
        channel = str(message.channel)

        if username not in RPS_dict:
            RPS_dict[username] = 0
            RPS_dict[username + "bot"] = 0

        print(f'{username} said: "{user_message}" ({channel})')

        try:
            response = responses.get_response(user_message)
            #Play rock paper scissors and Hangman
            if booly:
                word = random.choice(web2lowerset)
                empty = len(word)
                await message.channel.send("guesses remaining: ", guesses, "\n\n", "Letters in word: ","_" * empty)

            elif response == "RPS":
                #return rock, paper or scissors
                computer_choice = RPS_list[random.randint(0,2)]

                if user_message.lower() == computer_choice:
                    await message.channel.send(f'Computer choice: {computer_choice}\nIt is a Tie!\nScore: {username} {RPS_dict[username]} | Computer {RPS_dict[username + "bot"]}')
                elif user_message.lower() == "rock" and computer_choice == "scissors":
                    RPS_dict[username] += 1
                    await message.channel.send(f'Computer choice: {computer_choice}\n{username} Wins!\nScore: {username} {RPS_dict[username]} | Computer {RPS_dict[username + "bot"]}')
                elif user_message.lower() == "rock" and computer_choice == "paper":
                    RPS_dict[username + "bot"] += 1
                    await message.channel.send(f'Computer choice: {computer_choice}\nThe computer Wins!\nScore: {username} {RPS_dict[username]} | Computer {RPS_dict[username + "bot"]}')
                elif user_message.lower() == "paper" and computer_choice == "rock":
                    RPS_dict[username] += 1
                    await message.channel.send(f'Computer choice: {computer_choice}\n{username} Wins!\nScore: {username} {RPS_dict[username]} | Computer {RPS_dict[username + "bot"]}')
                elif user_message.lower() == "paper" and computer_choice == "scissors":
                    RPS_dict[username + "bot"] += 1
                    await message.channel.send(f'Computer choice: {computer_choice}\nThe computer Wins!\nScore: {username} {RPS_dict[username]} | Computer {RPS_dict[username + "bot"]}')
                elif user_message.lower() == "scissors" and computer_choice == "paper":
                    RPS_dict[username] += 1
                    await message.channel.send(f'Computer choice: {computer_choice}\n{username} Wins!\nScore: {username} {RPS_dict[username]} | Computer {RPS_dict[username + "bot"]}')
                elif user_message.lower() == "scissors" and computer_choice == "rock":
                    RPS_dict[username + "bot"] += 1
                    await message.channel.send(f'Computer choice: {computer_choice}\nThe computer Wins!\nScore: {username} {RPS_dict[username]} | Computer {RPS_dict[username + "bot"]}')

            elif response == "HANGMAN":
                booly = True
        
            elif user_message.lower() == "!help":
                await message.channel.send(response)

            else:
                await message.channel.send(response)
        except Exception as e:
            print(e)

    client.run(os.getenv("token"))