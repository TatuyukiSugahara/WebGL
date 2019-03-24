import math

rout_list = [[0, 50, 80, 0, 0], [0, 0, 20, 15, 0 ], [0, 0, 0, 10, 15], [0, 0, 0, 0, 30], [0, 0, 0, 0, 0]] # 初期のノード間の距離のリスト

#ノードの数。
node_num = len(rout_list) 

# 未探索ノード([0,1,2,3,4])。
unsearched_nodes = list(range(node_num))
# ノードごとの距離のリスト(浮動小数の正の無限大を入れている。)。
distance = [math.inf] * node_num
# 最短経路でそのノードのひとつ前に到達するノードのリスト(-1で初期化)。
previous_nodes = [-1] * node_num
# 初期のノードの距離は0。
distance[0] = 0 

def get_target_min_index(min_index, distance, unsearched_nodes):
    start = 0
    while True:
        index = distance.index(min_index, start)
        found = index in unsearched_nodes
        # 未探索ノードにインデックスがあれば。
        if found:
            # それが最小のインデックス。
            return index
        else:
            # ないので次へ。
            start = index + 1

#未探索ノードがなくなるまで繰り返す。
while(len(unsearched_nodes) != 0): 
    # まず未探索ノードのうちdistanceが最小のものを選択する。
    # 最小のdistanceを見つけるための一時的なdistance。初期値は inf に設定。
    posible_min_distance = math.inf 
    # 未探索のノードのループ。
    for node_index in unsearched_nodes: 
        if posible_min_distance > distance[node_index]: 
            # より小さい値が見つかれば更新。
            posible_min_distance = distance[node_index] 
    # 未探索ノードのうちで最小のindex番号を取得。
    target_min_index = get_target_min_index(posible_min_distance, distance, unsearched_nodes) 
    # ここで探索するので未探索リストから除去。
    unsearched_nodes.remove(target_min_index) 

    # ターゲットになるノードからのびるエッジのリスト。
    target_edge = rout_list[target_min_index] 
    for index, route_dis in enumerate(target_edge):
        if route_dis != 0:
            if distance[index] > (distance[ target_min_index] + route_dis):
                # 過去に設定されたdistanceよりも小さい場合はdistanceを更新。
                distance[index] = distance[ target_min_index] + route_dis 
                #　ひとつ前に到達するノードのリストも更新。
                previous_nodes[index] =  target_min_index 


# 結果。
print("経路")
previous_node = node_num - 1
while previous_node != -1:
    if previous_node !=0:
        print(str(previous_node + 1) + " <- ", end='')
    else:
        print(str(previous_node + 1))
    previous_node = previous_nodes[previous_node]

print("距離")
print(distance[node_num - 1])