# データ前処理用関数
# データの結合、重複削除には氏名列を使用する
# ["氏名", "性別"]という列名を使用すること
import pandas as pd
import numpy as np

# データ読み込み用関数
# "氏名"列に基づいて、データの結合および削除を行う
def read(path):
    data = pd.read_csv(path)
    data["氏名"] = data["氏名"].str.replace('\s', '', regex=True).values
    data = data.drop_duplicates(subset="氏名")
    return data.reset_index(drop=True)

# データ削除用関数
# レクの幹事等、チーム分けに使用しない人物を削除する
def remove(main_data, remove_data):
    remove_list = remove_data["氏名"].values
    data = main_data[~(main_data["氏名"].isin(remove_list))]
    return data.reset_index(drop=True)

# データ分割用関数
# 会場数を複数にする場合に参加者をnum等分する
def split(data, num):
    length = len(data)
    dataList = []
    for i in range(num):
        if i != num-1:
            dataList.append(data.iloc[length//num*i:length//num*(i+1)])
        else:
            dataList.append(data.iloc[length//num*i:])
    return dataList
