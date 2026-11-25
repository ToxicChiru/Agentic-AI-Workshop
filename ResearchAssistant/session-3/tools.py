
import csv
from pathlib import Path


# Tool 1: Calculator
def calculator(operation, numbers):

    try:
        if not numbers:
            return "Please provide at least one number."

        if operation == "sum":
            return sum(numbers)

        elif operation == "average":
            return sum(numbers) / len(numbers)

        elif operation == "maximum":
            return max(numbers)

        elif operation == "minimum":
            return min(numbers)

        else:
            return "Unsupported operation."

    except Exception as e:
        return f"Calculation error: {e}"


# Tool 2: Search the research dataset
def search_dataset(query):

    file_path = Path(__file__).parent / "research_data.csv"

    try:
        results = []

        with open(file_path, "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)

            for row in reader:
                searchable_text = " ".join(row.values()).lower()

                if query.lower() in searchable_text:
                    results.append(row)

        if results:
            return results

        return "No matching records found."

    except FileNotFoundError:
        return "Research dataset file was not found."


# Tool 3: Retrieve information about a research topic
def retrieve_information(topic):

    file_path = Path(__file__).parent / "research_data.csv"

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)

            for row in reader:
                if row["topic"].lower() == topic.lower():
                    return row

        return f"No information available for {topic}."

    except FileNotFoundError:
        return "Research dataset file was not found."
