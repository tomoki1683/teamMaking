# データ前処理用関数
# データの結合、重複削除には氏名列を使用する
# ["氏名", "性別"]という列名を使用すること
import pandas as pd
import math

# 定義した関数群を用いて、データの前処理を行う関数
def main(main_path, remove_path, zoom_num):
    main_data = read(main_path)
    remove_data = read(remove_path)
    data = remove(main_data, remove_data)
    male_data = data[data["性別"] == "男"]
    female_data = data[data["性別"] == "女"]
    maleDataList = split(male_data, zoom_num)
    femaleDataList = split(female_data, zoom_num)
    return maleDataList, femaleDataList

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

# チーム作成用の情報出力関数
def inform(male_data, female_data, t_num, m_num):
    totalMember_num = len(male_data) + len(female_data)
    # チーム数が先に決まっている場合
    if t_num > 0:
        team_num = t_num
        if totalMember_num % team_num == 0:
            teamMember_num = totalMember_num // team_num
            shortage = 0
        else:
            teamMember_num = totalMember_num // team_num + 1
            shortage = team_num * teamMember_num - totalMember_num
        totalMember_num += shortage
    # 1チームのメンバー数が先に決まっている場合
    else:
        teamMember_num = m_num
        if totalMember_num % teamMember_num == 0:
            team_num = totalMember_num // teamMember_num
            shortage = 0
        else:
            team_num = math.ceil(totalMember_num / teamMember_num)
            shortage = teamMember_num - totalMember_num % teamMember_num
        totalMember_num += shortage
    information = [totalMember_num, team_num, teamMember_num, shortage]
    return information

# 出力用DF作成関数
def make_outputDF(male_data, female_data, shortage):
    # 参加者ダミーを作成し、出力用DFを作成する
    # ダミーの作成方法は、元データの入り方によって変える
    dammyDF = pd.DataFrame([["ダミー" + str(i+1), "ダミー" + str(i+1), "なし", "なし", "なし"] for i in range(shortage)], columns=male_data.columns)
    outputDF = pd.concat([male_data, female_data, dammyDF]).reset_index(drop=True)
    return outputDF