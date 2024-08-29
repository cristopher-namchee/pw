def format_sql_table(data: str) -> str:
    """
    Formats a string representing an SQL table into a string of aligned columns.

    Args:
        data (str): A string representing an SQL table with one or more lines of data.

    Returns:
        str: A string representing the formatted SQL table.

    """
    lines = [line.strip() for line in data.strip().splitlines() if line.strip()]

    headers = lines[0].split()

    data = [line.split() for line in lines[1:]]

    max_status_length = max(len(headers[0]), max(len(row[0]) for row in data))
    max_count_length = max(len(headers[1]), max(len(row[1]) for row in data))

    table = []
    table.append(f"+{'-' * (max_status_length + 2)}+{'-' * (max_count_length + 2)}+")
    table.append(
        f"| {headers[0].ljust(max_status_length)} | {headers[1].rjust(max_count_length)} |"
    )
    table.append(f"+{'-' * (max_status_length + 2)}+{'-' * (max_count_length + 2)}+")

    for row in data:
        table.append(
            f"| {row[0].ljust(max_status_length)} | {row[1].rjust(max_count_length)} |"
        )

    table.append(f"+{'-' * (max_status_length + 2)}+{'-' * (max_count_length + 2)}+")

    return "\n".join(table)
