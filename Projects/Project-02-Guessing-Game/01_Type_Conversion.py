age = input ("Please enter your age: ")
age = int(age)
print("Your age is: ", age)

# professional way of doing the same thing
age = int(input ("Please enter your age: "))
print("Your age is: ", age)


# Exercise 1 (Easy)

# Write a program that:

# asks the user for two numbers
# converts them to integers
# prints their sum

num1 = int(input("Enter the first number: "))
num2 = int(input("Enter the second number: "))
sum = num1 + num2
print("The sum of the two numbers is: ", sum)

# Exercise 2 (Medium)

# Write a program that:

# asks user for birth year
# calculates age in 2026
# prints the result

birth_year = int(input("Please enter your birth year: "))
age_in_2026 = 2026 - birth_year
print("Your age in 2026 will be: ", age_in_2026)

