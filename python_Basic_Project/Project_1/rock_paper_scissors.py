import random

"""
    Rock Paper Scissors is a classic game that resonates with folks from around the world.
    It's a game where the user plays a round of Rock, Paper, Scissors against the computer.
Rules:
    - Rock beats Scissors.
    - Scissors beats Paper.
    - Paper beats Rock.
    Let's have fun together !!!
"""

# Mapping numbers to choices
choices = {1: "✊", 2: "✋", 3: "✌️"}

print("1 is for '✊' (Rock).")
print("2 is for '✋' (Paper).")
print("3 is for '✌️' (Scissors).")

player = int(input('Select one number between 1 and 3: '))
print(f'You picked: {choices.get(player, "Invalid choice")}')
computer = random.randint(1, 3)
print(f'The CPU picked: {choices[computer]}')

if player == computer:
    print("It's a tie!")
elif (player == 1 and computer == 3) or (player == 2 and computer == 1) or (player == 3 and computer == 2):
    print('The player won!')
elif player in [1, 2, 3]:
    print('The CPU won!')
else:
    print("Invalid input.")


'''
The second games is same that follows the same logic but this times with Rock, Paper, Scissors, Lizard and Spock

Rules: 
The rules follow the classic “Rock Paper Scissors” game, but with two new choices – “Lizard” and “Spock”:

Scissors cut Paper.
Paper covers Rock.
Rock crushes Lizard.
Lizard poisons Spock.
Spock smashes Scissors.
Scissors beat Lizard.
Lizard eats Paper.
Paper disproves Spock.
Spock vaporizes Rock.
Rock breaks Scissors.

'''

# Mapping numbers to choices
choices = {1: "✊", 2: "✋", 3: "✌️", 4: "🦎", 5: "🖖"}

print("1 is for '✊' (Rock).")
print("2 is for '✋' (Paper).")
print("3 is for '✌️' (Scissors).")
print("4 is for '🦎' (Lizards).")
print("5 is for '🖖' (Spock).")

player = int(input('Select one number between 1 and 5: '))
print(f'You picked: {choices.get(player, "Invalid choice")}')
computer = random.randint(1, 5)
print(f'The CPU picked: {choices[computer]}')


# Define all winning combinations for the player
winning_combinations = [
    (1, 3), # Rock crushes Scissors
    (1, 4), # Rock crushes Lizard
    (2, 1), # Paper covers Rock
    (2, 5), # Paper disproves Spock
    (3, 2), # Scissors cut Paper
    (3, 4), # Scissors decapitate Lizard
    (4, 2), # Lizard eats Paper
    (4, 5), # Lizard poisons Spock
    (5, 1), # Spock vaporizes Rock
    (5, 3)  # Spock smashes Scissors
]

if player == computer:
    print("It's a tie!")
elif (player, computer) in winning_combinations:
    print('The player won!')
elif player in [1, 2, 3, 4, 5]:
    print('The CPU won!')
else:
    print("Invalid input.")