import dataPreprocessing as dp
from groupMaking import make

# 取得するデータのパスを記載する
# 適宜、書き換える
main_path = "../../testData.csv"
remove_path = "../../fix_zoom幹事リスト.csv"
zoom_num = 2

# データの前処理を行う
main_data = dp.read(main_path)
remove_data = dp.read(remove_path)
data = dp.remove(main_data, remove_data)
male_data = data[data["性別"] == "男"]
female_data = data[data["性別"] == "女"]
maleDataList = dp.split(male_data, zoom_num)
femaleDataList = dp.split(female_data, zoom_num)

# チーム分けを行う
for i in range(zoom_num):
    # 必要な情報を定義する
    # 適宜、書き換える
    team_num = 25
    teamMember_num = 0
    teamList, memberList = make.makeGroup_sequence(maleDataList[0], femaleDataList[0], team_num, teamMember_num)
    print(memberList)

