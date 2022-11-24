from mongoDBConnector import get_database
import pandas as pd
import csv
import subprocess

if __name__ == '__main__':
    db = get_database()
    collection_name = db["twitch_games"]

    df = pd.read_csv(r'../Project1/data/Twitch_game_data.csv', encoding='cp1252')
    print(df)

    collection_name.insert_many(df.to_dict('records'))

    ddmp = subprocess.call(
        'cat data/alcohol-consumption-vs-gdp-per-capita.csv | ' + \
        './damaged_data_mapper.py | ' + \
        './damaged_data_reducer.py > ' + \
        'output.csv', shell=True)
