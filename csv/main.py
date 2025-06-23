import csv
import os

def read_csv(file_path):
    """Reads a CSV file and returns its content as a list of dictionaries."""
    with open(file_path, mode='r') as csvfile:
        reader = csv.DictReader(csvfile)
        rows = []
        for row in reader:
            rows.append(row)
        return rows

result = read_csv(os.path.dirname(__file__) + '/pokemon.csv')
