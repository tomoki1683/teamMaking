# 最適化用の関数を定義する
# チームnにおける重複度
def calc_team_cost(n, gender_count_by_team, team_to_member, sameTeam_list, womenLess_list):
    
    g = 0
    s = 0
    #d = 0
    w = 0
    team = team_to_member[n]
    
    # 性別の重複度：男女の人数差の二乗
    g = abs(gender_count_by_team[n]['男'] - gender_count_by_team[n]['女']) ** 2

    # チーム構成の重複度：過去にチームメンバー同士が同じチームになった回数*10
    for i in range(len(team)):
        m1 = team[i]
        for j in range(i+1,len(team)):
            m2 = team[j]
            s += sameTeam_list[m1][m2] * 10
    
    # ダミー人間の重複度：ダミー人数の二乗
    #d = gender_count_by_team[n]['なし'] ** 4
    
    # 女性少数チームの重複度：過去に少数チームになった回数*(5 - 現在の女性人数)
    now_woman = gender_count_by_team[n]['女']
    for i in team:
        w += womenLess_list[i] * (5-now_woman)
    
    return g + s + w