# 找到 AN 中检测能力好的点
# 只针对特定的算法来说

# find the decGood node in AN:
def decFaultFree(self):
    # print("正在寻找AN中检测能力好的点")
    self.faultFreeSet = [] #这个是在算法一中检测出来 检测能力好的点, 跟之前网络生成的 self.faulFreeSetAN = [] 结果大概率是一样的
    bad_list=[]
    #这部分的做法是: 遍历G_AN_H的网络的每一个邻居,将检测合格的AN点放入一个叫faultFreeSet集合中,
    #G_AN_H有两个点G1, G2都与AN中没有检测能力的点 A1有相邻关系
    #如果A1在遍历G1邻居的时候恰好通过随机的方式进入faultFreeSet, 但是在遍历G2邻居的时候,也会把A1剔除优秀的集合
    #额外添加了一个bad_list用来记录AN中已经被证明检测能力有问题的点, 只要被打入到bad_list, 后续就不用再检测这个节点了

    for node in self.G_AN_H:
        for AN_node_id in node.neighbors[1]:
            if AN_node_id in bad_list:
                continue
            if self.Algorithm1(self.AN[AN_node_id], node):
                for node_id in self.AN[AN_node_id].neighbors[1]:
                    if not self.Algorithm1(self.AN[AN_node_id], self.AN[node_id]):
                        bad_list.append(AN_node_id)
                        break
                if AN_node_id in bad_list: continue
            #if self.AN[AN_node_id].returnDF():
                if self.AN[AN_node_id] not in self.faultFreeSet:
                    self.faultFreeSet.append(self.AN[AN_node_id])
            else:
                bad_list.append(AN_node_id)
                if self.AN[AN_node_id] in self.faultFreeSet:
                    self.faultFreeSet.remove(self.AN[AN_node_id])

    return self.faultFreeSet