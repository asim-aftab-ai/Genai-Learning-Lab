import random
secret_number = random.randint(1, 10)

while True:
    guess = int(input("Enter the number: "))

    if guess == secret_number:
        print("You win.")
        break
    elif guess > secret_number:
        print("Too high! Try again.")
    else:
        print("Too low! Try again.")
