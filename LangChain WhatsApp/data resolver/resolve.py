import csv
from pathlib import Path

path = Path(__file__).parent

csv_file_path = path / 'talk.csv'
output_txt_file_path =path.parent / 'realtime_ai_character' / 'character_catalog' / 'Rga' / 'output.txt'

with open(csv_file_path, newline='', encoding='utf-8') as csvfile, \
     open(output_txt_file_path, 'w', encoding='utf-8') as txtfile:

    csvreader = csv.reader(csvfile)
    next(csvreader, None)

    for row in csvreader:
        if len(row) >= 3:  
            first_column, second_column = row[1].strip(), row[2].strip()
            
            txtfile.write(f'[{first_column} -> {second_column}]\n')
