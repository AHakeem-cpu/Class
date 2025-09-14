from datetime import datetime, timedelta

# Define a custom exception for duplicate visitors
class DuplicateVisitorError(Exception):
    def __init__(self, name):
        self.message = f"Visitor '{name}' already signed in last! No back-to-back visits allowed."
        super().__init__(self.message)

# Define a custom exception for time restriction
class VisitTooSoonError(Exception):
    def __init__(self, last_time):
        self.message = f"Another visitor signed in less than 5 minutes ago at {last_time}. Please wait."
        super().__init__(self.message)

def main():
    filename = "visitors.txt"

    # Ensure the file exists
    try:
        with open(filename, "r", encoding="utf-8") as f:
            pass
    except FileNotFoundError:
        print("File not found, creating a new file")
        with open(filename, "w", encoding="utf-8") as f:
            pass

    visitor = input("Enter visitor's name: ").strip()

    try:
        with open(filename, "r", encoding="utf-8") as f:
            lines = f.readlines()

        if lines:
            last_line = lines[-1].strip()
            last_name, last_time_str = last_line.split(" | ")
            last_time = datetime.strptime(last_time_str, "%Y-%m-%d %H:%M:%S.%f")

            # Check for duplicate visitor
            if visitor == last_name:
                raise DuplicateVisitorError(visitor)

            # Check for 5-minute gap
            if datetime.now() - last_time < timedelta(minutes=5):
                raise VisitTooSoonError(last_time.strftime("%Y-%m-%d %H:%M:%S"))

        # Log the new visitor
        with open(filename, "a", encoding="utf-8") as f:
            f.write(f"{visitor} | {datetime.now()}\n")

        print("Visitor added successfully.")

    except (DuplicateVisitorError, VisitTooSoonError) as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
