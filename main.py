from mongoDBConnector import get_database
import pandas as pd
import csv
import subprocess
import matplotlib.pyplot as plt
import statsmodels.api as sm
import pylab


def get_data_from_db(conn):
    cursor = conn.find()
    rows = pd.DataFrame([x for x in cursor])
    rows.drop(columns=['_id'], inplace=True)
    return rows


def plot_hists(data_frame, path):
    data_frame.hist(column='Total alcohol consumption', bins=20, figsize=(20, 10))
    plt.savefig(f'{path}/hist_TAC.png')
    plt.clf()


def plot_box_plots(data_frame, path):
    data_frame.boxplot(column='Total alcohol consumption', figsize=(20, 10))
    plt.savefig(f'{path}/boxplot_TAC.png')
    plt.clf()


def plot_qqplot(data_frame, path):
    sm.qqplot(data_frame['Total alcohol consumption'], line='s')
    plt.savefig(f'{path}/qq_TAC.png')
    plt.clf()


def get_stats_for_df(data_frame, name):
    return {
        'name': name,
        'mean': data_frame["Total alcohol consumption"].mean(),
        'standard error': data_frame["Total alcohol consumption"].sem(),
        'median': data_frame["Total alcohol consumption"].median(),
        'standard deviation': data_frame["Total alcohol consumption"].std(),
        'variance': data_frame["Total alcohol consumption"].var(),
        'kurtosis': data_frame["Total alcohol consumption"].kurtosis(),
        'skewness': data_frame["Total alcohol consumption"].skew(),
        'min': data_frame["Total alcohol consumption"].min(),
        'max': data_frame["Total alcohol consumption"].max(),
        'sum': data_frame["Total alcohol consumption"].sum(),
        'number of records': data_frame["Total alcohol consumption"].size
    }


def save_plots(data_frame, path):
    plot_hists(data_frame, path)
    plot_box_plots(data_frame, path)
    plot_qqplot(data_frame, path)


if __name__ == '__main__':
    db = get_database()
    collection_name = db["alcohol_consumption"]
    stats_collection_name = db["alcohol_consumption_stats"]
    stats = []

    subprocess.call(
        'hdfs dfs -copyFromLocal ./data/alcohol-consumption-vs-gdp-per-capita.csv /user/kuba/project/input/',
        shell=True)

    subprocess.call(
        'hadoop jar ./jars/hadoop-streaming-2.7.3.jar ' + \
        '-input /user/kuba/project/input/alcohol-consumption-vs-gdp-per-capita.csv ' + \
        '-output /user/kuba/project/output ' + \
        '-mapper ./mapper.py ' + \
        '-reducer ./reducer.py',
        shell=True)

    subprocess.call(
        'hadoop fs -cat /user/kuba/project/output/* > ./output.csv',
        shell=True)

    collection_name.drop()
    stats_collection_name.drop()

    df = pd.read_csv(r'./output.csv', encoding='cp1252',
                     names=["Entity", "Code", "Year", "Total alcohol consumption", "GDP per capita"])
    collection_name.insert_many(df.to_dict('records'))

    records = get_data_from_db(collection_name)
    save_plots(records, './plots/all')
    stats.append(get_stats_for_df(records, 'all'))

    records_poor = records[records['GDP per capita'] < 13000]
    save_plots(records_poor, './plots/poor')
    stats.append(get_stats_for_df(records_poor, 'poor'))

    records_rich = records[records['GDP per capita'] >= 13000]
    save_plots(records_rich, './plots/rich')
    stats.append(get_stats_for_df(records_rich, 'rich'))

    stats_collection_name.insert_many(stats)

    print('Job finished successfully!')
