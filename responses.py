def get_response(message: str) -> str:
    lower_message = message.lower()

    if lower_message == "rock" or lower_message == "paper" or lower_message == "scissors":
        return "RPS"

    if lower_message == "hangman":
        return "HANGMAN"

    if lower_message == '!help':
        return '`This is a help message that you can modify.`'

    return 'I didn\'t understand what you wrote. Try typing "!help".'