import pandas as pd
 
FILE_PATH = "EdinetcodeDlInfo.csv"
 
 
# 5桁の証券コードを4桁に変更（先頭4文字）
def scode_edit(val):
    return val[:4]
 
 
if __name__ == '__main__':
 
 
    # ＥＤＩＮＥＴコード,提出者名,証券コードを読み込む（合計3列）
    df = pd.read_csv(FILE_PATH, encoding="cp932", usecols=[0, 6, 11],
                     names=('edinet_code', 'name', 'syoken_code'), dtype={"syoken_code": str}, skiprows=2)
 
    # 証券コードが欠損値（NaN）である行を削除
    df = df.dropna(how='any', axis=0)
    # 出力用のデータフレーム作成
    df_ex = df.copy()
    df_ex["security_code"] = df_ex["syoken_code"].apply(scode_edit)
 
    # csv出力
    df_ex.to_csv("output.csv", index=False)

