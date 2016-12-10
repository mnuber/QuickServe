import csv




with open('app/tagwork.csv', 'rb') as f:
    csvr = csv.reader(f)
    entries = []
    for i in csvr:
        print i[1].upper()
