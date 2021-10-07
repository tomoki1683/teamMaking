from copy import deepcopy

# メンバー同士が同じチームに属した回数を記録
def sameTeam_count(sameTeam_num, teamList_T):
    output = deepcopy(sameTeam_num)
    for team in teamList_T:
        for member_i in range(len(team)):
            member_1 = team[member_i]
            for member_j in range(member_i+1, len(team)):
                member_2 = team[member_j]
                output[member_1][member_2] += 1
                output[member_2][member_1] += 1
    return output

# 女性の数が少ないチームになった回数を記録
def womenLess_count(womenLess_list, team_ravel, gender_count_list):
    output = deepcopy(womenLess_list)
    min_woman = 100
    for row in gender_count_list:
        if min_woman > row["女"]:
            min_woman = row["女"]
    for i in range(len(team_ravel)):
        if gender_count_list[team_ravel[i]]["女"] == min_woman:
            output[i] += 1
    return output