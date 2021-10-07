import numpy as np
import random
from groupMaking import groupOptimizationClass as goc
from collections import defaultdict

# チーム番号を順番に振っていくことで、チーム作成を行う関数を定義する
def makeGroup_sequence(totalMember_num, team_num, teamMember_num, rolling):
    teamList = np.tile(np.arange(team_num), (teamMember_num,1))
    memberList = np.arange(totalMember_num).reshape(teamMember_num, team_num)
    if rolling > 0:
        for rolling in range(teamMember_num):
            teamList[rolling] = np.roll(teamList[rolling], -rolling**2)
            memberList[rolling] = np.roll(memberList[rolling], rolling**2)
    return teamList, memberList

# groupOptimizationClassを用いることで、チーム作成を行う関数を定義する
def makeGroup_optimize(information, outputDF, sameTeam_list, womenLess_list):
    random.seed(95)
    gender_count_by_team = [defaultdict(int) for _ in range(information[1])]
    teamList, memberList = makeGroup_sequence(information[0], information[1], information[2], 0)
    for j in range(information[0]):
        gender_count_by_team[teamList.ravel()[j]][outputDF["性別"].values[j]] += 1
    init_state = [list(teamList.ravel()), gender_count_by_team, memberList.T.tolist()]
    prob = goc.GroupingProblem(init_state, outputDF, sameTeam_list, womenLess_list)
    prob.steps = 10**4 * 3
    prob.copy_strategy = "deepcopy"
    _, _ = prob.anneal()
    return prob.state