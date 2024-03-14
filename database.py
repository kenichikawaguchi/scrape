import sqlite3
import my_csv


def get_db():
    conn = sqlite3.connect('db.sqlite3')
    # conn = sqlite3.connect('articles.db')
    return conn


'''
def init_db(df):
    print(df.columns)
    get_data_from_df(df)
    with sqlite3.connect('articles.db') as conn:
        conn.execute("DROP TABLE IF EXISTS COMPANY")
        df.to_sql('COMPANY', conn)
    print('データベースを初期化しました')


if __name__ == '__main__':
    df = my_csv.my_csv()
    init_db(df)

'''
