file_user = input("Enter file name: ")

try:
    with open(file_user, "r") as file:
        content = file.read()

    lines = content.splitlines()
    total_lines = len(lines)

    words = content.split()
    total_words = len(words)

    unique_words = set(words)
    total_unique_words = len(unique_words)

    print("\n--- File Summary ---")
    print("Total lines:", total_lines)
    print("Total words:", total_words)
    print("Total unique words:", total_unique_words)

except FileNotFoundError:
    print("File cannot be opened:", file_user)