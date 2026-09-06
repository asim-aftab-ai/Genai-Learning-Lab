# making a number guessing game my first game and program

import random

secret_number = random.randint(1, 10)

while True: 
    guess = int(input("Guess the number between 1 and 10: "))
    
    if guess == secret_number:
        print("You win.")
        break
    elif guess > secret_number:
        print("Too high! Try again.")
    else:
        print("Too low! Try again.")
        