from random import choice
from simanneal import Annealer
from copy import deepcopy
from groupMaking import cost_function

# チーム作成用のクラスを定義する
# 最適化を用いて、cost_function.pyで定義した値が最小となるようにチーム分けを行う
class GroupingProblem(Annealer):
    def __init__(self, init_state, outputDF, sameTeam_list, womenLess_list):
        super(GroupingProblem, self).__init__(init_state)  # important!
        self.outputDF = outputDF
        self.sameTeam_list = sameTeam_list
        self.womenLess_list = womenLess_list
        
    def move(self):
         
        # ランダムにa,bの２人選ぶ
        a = choice(range(len(self.state[0])))
        b = choice(range(len(self.state[0])))
        # 同一人物だった場合、何もせず終了(重複度の差分は0)
        if a == b:
            return 0
        # a,bそれぞれのチーム
        a_team = self.state[0][a]
        b_team = self.state[0][b]
        # ２人が同一チームだった場合、何もせず終了(重複度の差分は0)
        if a_team == b_team:
            return 0
         
        # 各チームのメンバー交換前の重複度
        cost_a_before = cost_function.calc_team_cost(a_team, self.state[1], self.state[2], self.sameTeam_list, self.womenLess_list)
        cost_b_before = cost_function.calc_team_cost(b_team, self.state[1], self.state[2], self.sameTeam_list, self.womenLess_list)
 
        # aのチームのaの性別の人数
        self.state[1][a_team][self.outputDF["性別"].values[a]] -= 1
        # bのチームのbの性別の人数
        self.state[1][b_team][self.outputDF["性別"].values[b]] -= 1
         
        # aのチームのリストからaを除く(効率悪いが横着)
        self.state[2][a_team].remove(a)
        # bのチームのリストからbを除く(効率悪いが横着)
        self.state[2][b_team].remove(b)

        # a,bの所属チームを交換
        self.state[0][a], self.state[0][b] = self.state[0][b], self.state[0][a]
 
        # aの新しいチームのaの性別の人数
        self.state[1][b_team][self.outputDF["性別"].values[a]] += 1
        # bの新しいチームのbの性別の人数
        self.state[1][a_team][self.outputDF["性別"].values[b]] += 1
         
        # aの新しいチームのリストにaを追加
        self.state[2][b_team].append(a)
        # bの新しいチームのリストにbを追加
        self.state[2][a_team].append(b)
        
        # 各チームのメンバー交換後の重複度
        cost_a_after = cost_function.calc_team_cost(a_team, self.state[1], self.state[2], self.sameTeam_list, self.womenLess_list)
        cost_b_after = cost_function.calc_team_cost(b_team, self.state[1], self.state[2], self.sameTeam_list, self.womenLess_list)
         
        # メンバー交換による重複度の差分を返す
        return cost_a_after - cost_a_before + cost_b_after - cost_b_before
              
    # 目的関数
    def energy(self):
        # 各チームの重複度の和を返す
        return sum(cost_function.calc_team_cost(i, self.state[1], self.state[2], self.sameTeam_list, self.womenLess_list) for i in range(len(self.state[1])))