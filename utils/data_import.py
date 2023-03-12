import csv

def import_data_to_csv(filename):
    data = []
    with open(filename) as f:
        reader = csv.reader(f, delimiter='\t')
        for row in reader:
            data.append(row)
    return data
