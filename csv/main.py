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

desired = []

result = read_csv(os.path.dirname(__file__) + '/pokemon.csv')
for row in result:
    if int(row["Sp. Atk"]) >= 150:
        desired.append(row)

def get_sp_atk(pokemon):
    return int(pokemon["Sp. Atk"])

desired.sort(key=get_sp_atk, reverse=True)
for pokemon in desired:
    print(pokemon["Name"], pokemon["Type 1"], pokemon["Type 2"], pokemon["Sp. Atk"])