def add(a, b):
  result = (a + b)
  return result

def subtract(a, b):
  result = (a - b)
  return result

def multiply(a, b):
  result = (a * b)
  return result

def divide(a, b):
  result = (a / b)
  return result

while True:
  print("1. add")
  print("2. subtract")
  print("3. multiply")
  print("4. divide")
  print("5. quit")
  choice=int(input("Enter your choise: "))
  if choice==5:
    break 
  if choice == 1:
    numb1 = int(input("Enter first number: "))
    numb2 = int(input("Enter second number: "))
    answer = add(numb1, numb2)
    print("The answer is:", answer)

  elif choice == 2:
      numb1 = int(input("Enter first number: "))
      numb2 = int(input("Enter second number: "))
      answer = subtract(numb1, numb2)
      print("The answer is:", answer)
    
  elif choice == 3:
        numb1 = int(input("Enter first number: "))
        numb2 = int(input("Enter second number: "))
        answer = multiply(numb1, numb2)
        print("The answer is:", answer)
    
  elif choice == 4:
        numb1 = int(input("Enter first number: "))
        numb2 = int(input("Enter second number: "))
        answer = divide(numb1, numb2)
        print("The answer is:", answer)