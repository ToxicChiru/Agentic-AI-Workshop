
import csv
import json
from pathlib import Path

from langchain_core.tools import tool


# Tool 1: Calculator
@tool
def calculator(operation: str, numbers: list[float]) -> str:
    """Perform numerical calculations: sum, average, maximum or minimum."""

    try:
        if not numbers:
            return "Please provide at least one number."

        if operation == "sum":
            result = sum(numbers)

        elif operation == "average":
            result = sum(numbers) / len(numbers)

        elif operation == "maximum":
            result = max(numbers)

        elif operation == "minimum":
            result = min(numbers)

        else:
            return "Unsupported operation."

        return str(result)

    except Exception as e:
        return f"Calculation error: {e}"


# Tool 2: Search the research dataset
@tool
def search_dataset(query: str) -> str:
    """Search search_dataset.csv and return matching topics and record counts."""

    file_path = Path(__file__).parent / "search_dataset.csv"

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            records = list(csv.DictReader(file))

        matches = [
            row for row in records
            if query.lower() in " ".join(
                value for value in row.values() if value is not None
            ).lower()
        ]
        topics = sorted({
            row["topic"] for row in matches
            if row.get("topic")
        })

        return json.dumps({
            "query": query,
            "matching_records": len(matches),
            "total_records": len(records),
            "relevant_topics": topics,
            "records": matches
        }, ensure_ascii=False)

    except FileNotFoundError:
        return f"Dataset file was not found: {file_path}"


# Tool 3: Retrieve a specific research topic
@tool
def retrieve_information(topic: str) -> str:
    """Retrieve the complete dataset record for a specific research topic."""

    file_path = Path(__file__).parent / "search_dataset.csv"

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)

            for row in reader:
                if row["topic"].lower() == topic.lower():
                    return str(row)

        return f"No information available for {topic}."

    except FileNotFoundError:
        return f"Dataset file was not found: {file_path}"


# Register all available tools
TOOLS = [
    calculator,
    search_dataset,
    retrieve_information
]
