import discord
import responses
import os
import random
from dotenv import load_dotenv
#load enviroment variables, these variables are used to store sensitive data
load_dotenv()

RPS_dict = dict()
RPS_list = ["rock", "paper", "scissors"]

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
            #Play rock paper scissors
            if response == "RPS":
                #return rock, paper or scissors
                computer_choice = RPS_list[random.randint(0,2)]

                if user_message == computer_choice:
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

        except Exception as e:
            print(e)

    client.run(os.getenv("token"))