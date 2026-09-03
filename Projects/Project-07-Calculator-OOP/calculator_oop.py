class Calculator:
    def __init__(self):
        # The history attribute to store past calculations
        self.history = []

    def add(self, a, b):
        result = a + b
        self.history.append(f"{a} + {b} = {result}")
        return result

    def subtract(self, a, b):
        result = a - b
        self.history.append(f"{a} - {b} = {result}")
        return result

    def multiply(self, a, b):
        result = a * b
        self.history.append(f"{a} * {b} = {result}")
        return result

    def divide(self, a, b):
        if b == 0:
            raise ValueError("Cannot divide by zero.")
        result = a / b
        self.history.append(f"{a} / {b} = {result}")
        return result

    def get_history(self):
        return self.history

    def clear_history(self):
        self.history = []


# Example usage
if __name__ == "__main__":
    calc = Calculator()

    calc.add(10, 5)
    calc.multiply(4, 2)
    calc.divide(20, 4)
    calc.subtract(15, 3)

    print("Calculation History:")
    for record in calc.get_history():
        print(record)