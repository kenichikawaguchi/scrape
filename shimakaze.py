# セッション変数の取得
from setting import session, Inspector

# Userモデルの取得
from user import User

# DBにレコードの追加
user = User()
user.name = '太郎'
session.add(user)

user = User()
user.name = '一郎'
session.add(user)

session.commit()

# usersテーブルのレコードを全て取得する
users = session.query(User).all()
print(Inspector.get_columns("users"))
for user in users:
    print(user.name)
    print(user.created_at)
    print(type(user.created_at))

