import random


def play_game():
    number = random.randint(1, 100)
    attempts = 0
    max_attempts = 10

    print("=== Number Guessing Game ===")
    print(f"I've picked a number between 1 and 100.")
    print(f"You have {max_attempts} attempts. Good luck!\n")

    while attempts < max_attempts:
        remaining = max_attempts - attempts
        try:
            guess = int(input(f"Attempt {attempts + 1}/{max_attempts} — Enter your guess: "))
        except ValueError:
            print("Please enter a valid number.\n")
            continue

        attempts += 1

        if guess < 1 or guess > 100:
            print("Out of range! Guess between 1 and 100.\n")
            attempts -= 1
            continue

        if guess == number:
            print(f"\nCorrect! You guessed it in {attempts} attempt(s)!")
            return True
        elif guess < number:
            print(f"Too low!  {remaining - 1} attempt(s) left.\n")
        else:
            print(f"Too high! {remaining - 1} attempt(s) left.\n")

    print(f"\nOut of attempts! The number was {number}.")
    return False


def main():
    while True:
        play_game()
        again = input("\nPlay again? (yes/no): ").strip().lower()
        if again not in ("yes", "y"):
            print("Thanks for playing!")
            break
        print()


if __name__ == "__main__":
    main()
