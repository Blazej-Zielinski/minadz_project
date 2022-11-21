from mongoDBConnector import get_database
import pandas as pd

if __name__ == '__main__':
    db = get_database()
    collection_name = db["twitch_games"]

    df = pd.read_csv(r'./data/Twitch_game_data.csv', encoding='cp1252')
    print(df)

    collection_name.insert_many(df.to_dict('records'))


