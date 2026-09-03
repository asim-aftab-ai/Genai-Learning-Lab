import os


class EmptyFileError(Exception):
    """Custom exception raised when a log file exists but has no content."""

    pass


def analyze_log_file(file_path: str) -> dict[str, int]:
    """Reads a log file and counts occurrences of INFO, WARNING, and ERROR.

    Demonstrates:
      - Specific error catching (FileNotFoundError, PermissionError)
      - Custom exception raising (EmptyFileError)
      - try / except / finally execution flow
    """
    counts = {"INFO": 0, "WARNING": 0, "ERROR": 0}
    file_handle = None

    try:
        # Check if file has zero bytes
        if os.path.exists(file_path) and os.path.getsize(file_path) == 0:
            raise EmptyFileError(f"The file '{file_path}' is empty.")

        # Attempt to open and read line-by-line
        file_handle = open(file_path, "r", encoding="utf-8")

        for line in file_handle:
            clean_line = line.strip()
            for level in counts.keys():
                if level in clean_line:
                    counts[level] += 1

        return counts

    except FileNotFoundError:
        print(f"[Error Handled] File not found: '{file_path}'. Please verify the path.")
        return counts

    except PermissionError:
        print(
            f"[Error Handled] Access denied: You do not have permission to read '{file_path}'."
        )
        return counts

    except EmptyFileError as e:
        print(f"[Custom Exception Handled] {e}")
        return counts

    except Exception as e:
        # Catch-all safety net for any other unanticipated issue
        print(f"[Unexpected Error Handled] An unexpected error occurred: {e}")
        return counts

    finally:
        # Guarantee resource cleanup regardless of success or crash
        if file_handle:
            file_handle.close()
            print("[Cleanup] Closed log file handle safely.")


def print_summary(counts: dict[str, int]) -> None:
    """Formats and prints the analysis result."""
    total = sum(counts.values())
    print("\n" + "=" * 30)
    print("      LOG SUMMARY REPORT")
    print("=" * 30)
    for level, count in counts.items():
        print(f"{level:<10}: {count}")
    print("-" * 30)
    print(f"{'TOTAL':<10}: {total}")
    print("=" * 30 + "\n")


if __name__ == "__main__":
    sample_file = "app.log"

    # Create a small sample log for testing if it doesn't already exist
    if not os.path.exists(sample_file):
        with open(sample_file, "w", encoding="utf-8") as f:
            f.write("INFO: Application started successfully.\n")
            f.write("INFO: Connecting to database pool.\n")
            f.write("WARNING: Response time is higher than 500ms.\n")
            f.write("ERROR: Failed to fetch data from API endpoint.\n")
            f.write("INFO: Retrying connection...\n")
            f.write("ERROR: Connection timed out.\n")

    print(f"Analyzing '{sample_file}'...")
    results = analyze_log_file(sample_file)
    print_summary(results)

    # Test error handling behavior: Missing file
    print("Testing missing file handling...")
    analyze_log_file("non_existent_file.log")