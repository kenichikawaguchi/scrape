import pandas as pd


def my_csv():
    df = pd.read_csv('index_list.csv', sep='|', encoding="utf-8")
    #df = df.dropna()
    return df


if __name__ == '__main__':
    my_csv()

