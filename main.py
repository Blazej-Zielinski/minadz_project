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

    data_frame.hist(column='GDP per capita', bins=20, figsize=(20, 10))
    plt.savefig(f'{path}/hist_GDP.png')
    plt.clf()


def plot_box_plots(data_frame, path):
    data_frame.boxplot(column='Total alcohol consumption', figsize=(20, 10))
    plt.savefig(f'{path}/boxplot_TAC.png')
    plt.clf()

    data_frame.boxplot(column='GDP per capita', figsize=(20, 10))
    plt.savefig(f'{path}/boxplot_GDP.png')
    plt.clf()


def plot_density(data_frame, path):
    data_frame['Total alcohol consumption'].plot.kde(figsize=(20, 10))
    plt.savefig(f'{path}/kde_TAC.png')
    plt.clf()

    data_frame['GDP per capita'].plot.kde(figsize=(20, 10))
    plt.savefig(f'{path}/kde_GDP.png')
    plt.clf()


def plot_qqplot(data_frame, path):
    sm.qqplot(data_frame['Total alcohol consumption'], line='s')
    plt.savefig(f'{path}/qq_TAC.png')
    plt.clf()

    sm.qqplot(data_frame['GDP per capita'], line='s')
    plt.savefig(f'{path}/qq_GDP.png')
    plt.clf()


if __name__ == '__main__':
    db = get_database()
    collection_name = db["alcohol_consumption"]

    # collection_name.drop()
    # df = pd.read_csv(r'./output.csv', encoding='cp1252',
    #                  names=["Entity", "Code", "Year", "Total alcohol consumption", "GDP per capita"])
    # collection_name.insert_many(df.to_dict('records'))

    # ddmp = subprocess.call(
    #     'cat data/alcohol-consumption-vs-gdp-per-capita.csv | ' + \
    #     './damaged_data_mapper.py | ' + \
    #     './damaged_data_reducer.py > ' + \
    #     'output.csv', shell=True)

    records = get_data_from_db(collection_name)

    all_path = './plots/all'
    plot_hists(records, all_path)
    plot_box_plots(records, all_path)
    plot_density(records, all_path)
    plot_qqplot(records, all_path)
    print(f'Kurtoza_all: {records["Total alcohol consumption"].kurtosis()}')
    print(f'Skośność_all: {records["Total alcohol consumption"].skew()}')

    records_poor = records[records['GDP per capita'] < 13000]
    records_rich = records[records['GDP per capita'] >= 13000]

    poor_path = './plots/poor'
    plot_hists(records_poor, poor_path)
    plot_box_plots(records_poor, poor_path)
    plot_density(records_poor, poor_path)
    plot_qqplot(records_poor, poor_path)
    print(f'Kurtoza_poor: {records_poor["Total alcohol consumption"].kurtosis()}')
    print(f'Skośność_poor: {records_poor["Total alcohol consumption"].skew()}')

    rich_path = './plots/rich'
    plot_hists(records_rich, rich_path)
    plot_box_plots(records_rich, rich_path)
    plot_density(records_rich, rich_path)
    plot_qqplot(records_rich, rich_path)
    print(f'Kurtoza_rich: {records_rich["Total alcohol consumption"].kurtosis()}')
    print(f'Skośność_rich: {records_rich["Total alcohol consumption"].skew()}')
