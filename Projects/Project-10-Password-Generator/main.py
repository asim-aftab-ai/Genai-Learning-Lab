import argparse
from generator import generate_password
from strength import evaluate_strength


def main():
    parser = argparse.ArgumentParser(
        description="Generate a secure random password."
    )

    # Command-line arguments
    parser.add_argument(
        "-l", "--length",
        type=int,
        default=12,
        help="Password length (default: 12)"
    )
    parser.add_argument(
        "-c", "--complexity",
        choices=["letters", "numbers", "symbols"],
        default="symbols",
        help="Complexity level: 'letters' (letters only), 'numbers' (+ numbers), 'symbols' (+ numbers & symbols)"
    )

    args = parser.parse_args()

    # Generation & Evaluation
    password = generate_password(args.length, args.complexity)
    strength = evaluate_strength(password)

    # Output
    print("-" * 35)
    print(f"Password : {password}")
    print(f"Length   : {args.length}")
    print(f"Strength : {strength}")
    print("-" * 35)


if __name__ == "__main__":
    main()