import random 

secret_number = random.randint(1, 10)   

attempts = 0
max_attempts = 5

print("Welcome to the Guessing Game! You have 5 attempts to guess the number between 1 and 10.")

while attempts < max_attempts:
    guess = int(input("Enter your guess: "))
    attempts += 1
    
    if guess == secret_number:
        print(f"Congratulations! You've guessed the number {secret_number} in {attempts} attempts!")
        break

    if guess % 2 == 0:
        print("You guessed an even number.")
    else:
        print("You guessed an odd number.")

    if guess < secret_number:
        print("Too low! Try again.")
    else:
        print("Too high! Try again.")

    print("Remaining attempts:", max_attempts - attempts)

else:
    print(f"Game over! The secret number was {secret_number}. Better luck next time!")

# Ask once
play_again = input("Do you want to play again? (yes/no): ")

if play_again == "yes":
    print("Restart the program to play again.")
else:
    print("Thanks for playing!")