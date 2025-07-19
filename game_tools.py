import random
from agents import function_tool


def roll_dice() -> int:
    return random.randint(1, 20)

def generate_event() -> str:
    events = [
        "a secret door creaks open revealing a hidden staircase.",
        "a ghostly whisper warns of danger ahead.",
        "a river of lava blocks the path.",
        "a merchant appears offering magical goods.",
        "a strange puzzle blocks the corridor.",
        "a sudden cave-in changes the dungeon path.",
    ]
    return random.choice(events)


@function_tool
def roll_dice_tool() -> int:
    return roll_dice()


@function_tool
def generate_event_tool() -> str:
    return generate_event()
