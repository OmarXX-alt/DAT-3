def checkGuess(guess, number):
    if guess == number:
        return {
            "result": "correct",
            "message": "Correct! The number was " + str(number),
        }

    difference = abs(guess - number)
    if guess < number:
        return {
            "result": "higher",
            "message": "Too low, but you are warm." if difference <= 10 else "Too low, try again.",
        }

    return {
        "result": "lower",
        "message": "Too high, but you are warm." if difference <= 10 else "Too high, try again.",
    }


def createNumber():
    import random

    return random.randint(1, 100)

