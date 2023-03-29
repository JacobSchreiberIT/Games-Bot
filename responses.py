def get_response(message: str) -> str:
    lower_message = message.lower()

    if lower_message == "rock" or lower_message == "paper" or lower_message == "scissors":
        return "RPS"

    if lower_message == "hangman":
        return "HANGMAN"

    if lower_message == '!help':
        return '-Enter "rock", "paper" or "scissors" to play rock paper scissors\n'\
'-Enter "hangman" to play the game hangman'

    return 'I didn\'t understand what you wrote. Try typing "!help" for a list of commands.'