import csv
import sys
from datetime import datetime


def sort_puzzles_by_solving_time(csv_file_path):
    """
    Reads puzzle data from a CSV file, sorts it by solving time,
    and prints the puzzle dates in ascending order of solving time.

    Args:
        csv_file_path (str): The path to the CSV file.

    Returns:
        None. Prints the sorted puzzle dates to the console.
    """
    puzzles = []
    try:
        with open(csv_file_path, "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            if not reader.fieldnames:
                print("Error: The CSV file is empty or has no headers.")
                return

            print(f"Successfully read data from {csv_file_path}.  Now processing...")

            for row in reader:
                solving_seconds = row.get("solving_seconds")
                if not solving_seconds:
                    continue  # Skip this row if 'solving_seconds' is missing
                try:
                    solving_seconds = int(solving_seconds)
                except ValueError:
                    print(
                        f"Warning: Invalid solving_seconds value '{solving_seconds}'. Skipping row."
                    )
                    continue

                # skip impossibilities - even I'm not that good
                if solving_seconds < 2:
                    continue
                puzzles.append(
                    {
                        "print_date": row.get("print_date"),
                        "solving_seconds": solving_seconds,
                    }
                )
    except FileNotFoundError:
        print(f"Error: File not found at {csv_file_path}")
        return
    except Exception as e:
        print(f"An error occurred while reading the CSV file: {e}")
        return

    # Sort the puzzles by solving time
    puzzles.sort(key=lambda x: x["solving_seconds"])

    # Print the sorted puzzle dates
    if not puzzles:  # checks if the puzzles list is empty
        print("No puzzles to display.")
        return
    print("Top 100 fastest mini solves:")
    for i, puzzle in enumerate(puzzles[:99]):
        # Parse and format the date string
        date_obj = datetime.strptime(puzzle["print_date"], "%Y-%m-%d")
        formatted_date = date_obj.strftime("%B %d, %Y")
        link = f"https://www.nytimes.com/crosswords/game/mini/{date_obj.year}/{date_obj.month:02d}/{date_obj.day:02d}"  # zero pad month and day

        indent = " " * (len(str(i)) + 2)

        print(f"{i + 1}. Date: {formatted_date}")
        print(f"{indent}Solving Time: {puzzle['solving_seconds']} seconds")
        print(f"{indent}Link: {link}")


def main():
    """
    Main function to execute the script.
    Gets the CSV file path from the command line and calls the
    function to sort and print the puzzle dates.
    """
    if len(sys.argv) != 2:
        print("Usage: python script.py <csv_file_path>")
        return
    csv_file_path = sys.argv[1]
    sort_puzzles_by_solving_time(csv_file_path)


if __name__ == "__main__":
    main()
