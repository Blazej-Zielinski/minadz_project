#!/usr/bin/env python
import sys
import csv
import string

def extract_country(matrix, i):
    return [row[i] for row in matrix]

def find_latest_country_data(matrix):
    max_year = 0
    max_row = None
    for row in matrix:
        if int(row[2]) > max_year:
            max_year = int(row[2])
            max_row = row

    return max_row

def find_latest_data(matrix):
    latest_data = []
    unique_countries = list(set(extract_country(matrix, 0)))
    for unique_country in unique_countries:
        records = [row for row in matrix if row[0] == unique_country]
        latest_data.append(find_latest_country_data(records))

    return latest_data
    

not_damaged_lines = []

for line in sys.stdin:
    line = line.strip()
    values = line.split(',')
    values = list(filter(None, values))
    if len(values) == 5:
        not_damaged_lines.append(values)

latest = find_latest_data(not_damaged_lines)

for row in latest:
    print(*row, sep=',')
