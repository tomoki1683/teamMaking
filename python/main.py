import dataPreprocessing as dp
from groupMaking import make_method
from groupMaking import check_function as cf
import numpy as np
import pandas as pd
from collections import defaultdict
from copy import deepcopy

# 取得するデータのパスを記載する
# 適宜、書き換える
main_path = "../testData/testData_all.csv"
remove_path = "../testData/testData_remove.csv"
zoom_num = 2
group_information = [
    # [team_num, teamMember_num, make_method]
    [25, 0, "seq"],
    [0, 5, "seq"],
    [0, 5, "opt"]
]
alphabet = [1]
# データの前処理を行う
maleDataList, femaleDataList = dp.main(main_path, remove_path, zoom_num)

# チーム分けを行う
for zoom_room in range(zoom_num):
    print("")
    print(zoom_room, "つ目の会場用、作成開始")
    # 必要情報を事前に定義する
    information = dp.inform(maleDataList[zoom_room], femaleDataList[zoom_room], group_information[0][0], group_information[0][1])
    outputDF = dp.make_outputDF(maleDataList[zoom_room], femaleDataList[zoom_room], information[3])
    sameTeam_list = np.zeros((information[0], information[0]))
    womenLess_list = np.zeros(information[0])
    # チーム分けを行う
    for step in range(len(group_information)):
        information = dp.inform(maleDataList[zoom_room], femaleDataList[zoom_room], group_information[step][0], group_information[step][1])
        outputDF = outputDF.iloc[:information[0]]
        gender_count_by_team = [defaultdict(int) for _ in range(information[1])]
        if group_information[step][2] == "seq":
            teamList, memberList = make_method.makeGroup_sequence(information[0], information[1], information[2], 0)
            outputDF["チーム" + str(step+1) + "回目"] = teamList.ravel()
            sameTeam_list = cf.sameTeam_count(sameTeam_list, memberList.T)
            for j in range(information[0]):
                gender_count_by_team[teamList.ravel()[j]][outputDF["性別"].values[j]] += 1
            womenLess_list = cf.womenLess_count(womenLess_list, teamList.ravel(), gender_count_by_team)
            # 男女比を表示する
            print("")
            print(step+1, "回目のチーム作成終了")
            print(gender_count_by_team)
        elif group_information[step][2] == "opt":
            state = make_method.makeGroup_optimize(information, outputDF, sameTeam_list, womenLess_list)
            sameTeam_list = cf.sameTeam_count(sameTeam_list, state[2])
            womenLess_list = cf.womenLess_count(womenLess_list, state[0], state[1])
            # 男女比を表示する
            print("")
            print(step+1, "回目のチーム作成終了")
            gender_count_by_team = [defaultdict(int) for _ in range(information[1])]
            for i in range(information[0]):
                gender_count_by_team[state[0][i]][outputDF["性別"].values[i]] += 1
            print(gender_count_by_team)
            outputDF["チーム" + str(step+1) + "回目"] = state[0]
    # 重複している回数を計算する
    print("重複している回数 : ", np.count_nonzero(sameTeam_list >= 2)//2)
    # 女性少数チームの回数を計算する
    print("女性少数が全部続いた人の数", np.count_nonzero(womenLess_list == len(group_information))//2)
    # ダミーを除外する
    # ダミーを残しておくと、参加者が急遽増えた際は埋め込むだけで良いので対応しやすい
    outputDF = outputDF[outputDF["性別"] != "なし"]
    # チーム分けの全体結果をCSVで出力する
    useColumn = ["氏名"] + ["チーム" + str(i+1)  + "回目" for i in range(len(group_information))]
    outputDF = outputDF.loc[:,useColumn]
    for i in range(len(group_information)):
        if i+1 in alphabet:
            outputDF["チーム" + str(i+1)  + "回目"] = outputDF["チーム" + str(i+1)  + "回目"].apply(lambda c: chr(c+65))
        else:
            outputDF["チーム" + str(i+1)  + "回目"] = outputDF["チーム" + str(i+1)  + "回目"].apply(lambda n: n+1)
    outputDF.to_csv("../testResult/"+chr(zoom_room+65)+"会場チームリスト.csv")
    # チーム分けの個別結果をCSVで出力する
    for i in range(len(group_information)):
        # ピボットするために、["何人目"]列を追加する
        teamSTR = "チーム"+ str(i+1) +"回目"
        copy = deepcopy(outputDF.loc[:,["氏名", teamSTR]])
        copy["何人目"] = copy.groupby(teamSTR).cumcount() + 1
        #ピボットする
        copy.pivot(index=teamSTR, columns="何人目", values="氏名").to_csv("../testResult/"+chr(zoom_room+65)+"会場_"+teamSTR+"リスト.csv")

# 会場をCSVで出力する
roomDF = pd.DataFrame()
for zoom_room in range(zoom_num):
    roomX = pd.concat([maleDataList[zoom_room].loc[:,["氏名"]], femaleDataList[zoom_room].loc[:,["氏名"]]])
    roomX["グループ"] = chr(zoom_room+65)
    roomDF = pd.concat([roomDF, roomX])
roomDF.to_csv("../testResult/会場リスト.csv")