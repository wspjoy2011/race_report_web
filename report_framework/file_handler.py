"""
File handler module return data txt files
"""


def read_data_fromfile(filename: str) -> list[str]:
    """Read data from txt file"""
    data = []
    with open(filename, 'r') as file:
        for row in file:
            if row.rstrip():
                data.append(row.rstrip())
    return data
