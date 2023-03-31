def get_response(message: str) -> str:
    if message == "rock" or message == "paper" or message == "scissors":
        return "RPS"

    if message == "hangman":
        return "HANGMAN"

    if message == "gaming hangman":
        return "GAMING HANGMAN"

    if message == '!help':
        return '-Enter "rock", "paper" or "scissors" to play rock paper scissors\n'\
'-Enter "hangman" to play the game hangman\n'\
'-Enter "gaming hangman" to play hangman with video game words'

    return 'I didn\'t understand what you wrote. Try typing "!help" for a list of commands.'