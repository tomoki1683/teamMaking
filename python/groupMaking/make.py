import math
import numpy as np

# 出力用DFを作成する関数を定義する
def make_outputDF(male_data, female_data):
    return outputDF

# チーム番号を順番に振っていくことで、チーム作成を行う関数を定義する
def makeGroup_sequence(male_data, female_data, t_num, m_num):
    # 事前の情報定義
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
    # チーム作成
    teamList = np.tile(np.arange(team_num), (teamMember_num,1))
    memberList = np.arange(totalMember_num).reshape(teamMember_num, team_num)
    return teamList, memberList

# groupOptimizationClassを用いることで、チーム作成を行う関数を定義する
def makeGroup_optimize():
    return