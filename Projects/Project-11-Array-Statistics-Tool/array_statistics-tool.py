import numpy as np

print("======================================")
print("       NUMPY ARRAY STATISTICS TOOL")
print("======================================")

# Get numbers from the user
user_input = input("\nEnter numbers separated by spaces: ")

# Convert the user's input into numbers
numbers = np.array([float(x) for x in user_input.split()])

# Calculate statistics
mean = np.mean(numbers)
median = np.median(numbers)
std_dev = np.std(numbers)
minimum = np.min(numbers)
maximum = np.max(numbers)

# Display results
print("\n========== RESULTS ==========")

print(f"Number of values: {len(numbers)}")
print(f"Mean:              {mean:.2f}")
print(f"Median:            {median:.2f}")
print(f"Standard Deviation:{std_dev:.2f}")
print(f"Minimum:           {minimum:.2f}")
print(f"Maximum:           {maximum:.2f}")

print("==============================")