# 第二次重构完的网络基础模板
# 至少有一个邻居
import random

from Node.Node import Node
from utils.randomGenerateNetForDecGood import randomGenerateNetForDecGood
from utils.distribute import distribute
from utils.reload import *


class Network1(object):
    def __init__(self, parameters):
        self.H_p = parameters[0] # graph_id = 0 H_p的意思是 H 网络相关的参数
        [self.H_nodes_num, self.H_good_num, self.H_degree] = self.H_p
        self.H_all_degree = self.H_degree * self.H_nodes_num
        self.AN_p = parameters[1] # graph_id = 1
        [self.AN_nodes_num, self.AN_decGood_num, self.AN_degree] = self.AN_p
        self.AN_all_degree = self.AN_degree * self.AN_nodes_num

        self.G_AN_H_p = parameters[2] # graph_id = 2
        [self.G_AN_H_nodes_num] = self.G_AN_H_p

        self.node_p = parameters[3]
        [self.Node_level, self.g_goodN] = self.node_p

        self.H = []
        self.AN = []
        self.G_AN_H = []
        self.all_net = []
        #这边节点的命名排序是 H + AN + (G-AN-H), 统一有这个排序

        #生成网络的方式
        randomGenerateNetForDecGood(self) #在建模好点之间连线的时候, 所有网络都是相同的
        self.randomGenerateNetOthers() # AN 网络和其他的点之间的连线这个暂定每一家都一样

        self.H.sort(key=lambda x:x.node_id)
        self.AN.sort(key=lambda x:x.node_id)
        self.G_AN_H.sort(key=lambda x:x.node_id)

        self.all_node = self.H + self.AN + self.G_AN_H
        print("Network Has Been Generated!")
        #研究算法--这里导入要使用的算法即可, 传入 self 就好;因为参数其他的太多了

        # #看输出成果
        # printParameters(self)    

    def randomGenerateNetOthers(self):
        # 第零步 生成H中不好的节点, 并且加入到self.H 中
        #print("正在形成H中不好的点")
        #for index in range(self.H_nodes_num):
        #    if index not in self.faultFreeSetHids:
        #        node = Node(node_id=index, level=1, detection_function=False, goodN=0, degree=-1, graph_id=0)
        #        self.H.append(node)

        # 第一步 所有AN中的点都需要和 G_有一个连接
        # 1.1 首先选择AN中所有节点中, 哪些是检测能力好的点
        self.faulFreeSetAN = []
        self.faulFreeSetANids = []
        AN_ids = []

        start_node_id = self.H_nodes_num
        end_node_id = start_node_id + self.AN_nodes_num

        for index in range(start_node_id, end_node_id):
            AN_ids.append(index)

        # print("正在产生AN中检测能力好的点并且安排G_AN_H的邻居")
        while(len(self.faulFreeSetANids) != self.AN_decGood_num):
            i = random.randint(0, len(AN_ids)-1)
            node_id = AN_ids[i]
            node = Node(node_id=node_id, level=random.randint(1, self.Node_level), detection_function=True, goodN=0, degree=0, graph_id=1) #对它的好邻居个数没有要求
            self.AN.append(node)
            self.faulFreeSetAN.append(node)
            self.faulFreeSetANids.append(node_id)
            rangeJ = random.randint(0, len(self.G_AN_H)-1)
            node.addNeighbor(2, self.G_AN_H[rangeJ].node_id)
            self.AN_all_degree -=1
            self.G_AN_H[rangeJ].addNeighbor(1, i)
            AN_ids.remove(node_id)

        #1.2 剩下的AN中没有被选择的节点, 都是检测能力不好的点
        # print("正在随机将AN中检测能力不好的点生成邻居并且安排G_AN_H的邻居")
        for node_id in AN_ids:
            node = Node(node_id = node_id, degree=0, detection_function=False, goodN=0, level=random.randint(1, self.Node_level), graph_id=1)
            self.AN.append(node)
            rangeJ = random.randint(0, len(self.G_AN_H)-1)
            node.addNeighbor(2, rangeJ)
            self.G_AN_H[rangeJ].addNeighbor(1, node_id)
        self.AN_all_degree -= self.AN_nodes_num# 因为AN中每个点都需要和G_AN_H相连, 就先减去一个

        for index in range(self.H_nodes_num):
            if index not in self.faultFreeSetHids:
                node = Node(node_id=index, degree=-1, detection_function=False, goodN=0,
                            level=1, graph_id=0)
                self.H.append(node)

        # print("正在让H中某一个节点和AN中节点有连边")
        # 开始找邻居
        rangeI = random.randint(0, len(self.H)-1)
        rangeJ = random.randint(0, len(self.AN) - 1)
        node = self.H[rangeI]
        node.addNeighbor(1, rangeJ)
        self.AN[rangeJ].addNeighbor(0, node.node_id)
        self.AN_all_degree -= 1
        self.H_all_degree -= 1

        # 第三步, 将所有度进行划分, 理想是正态分布
        # print("正在给AN的节点划分度")
        an_degree = distribute( degree_sum=self.AN_all_degree, part_num=self.AN_nodes_num, covariance=self.AN_all_degree/self.AN_nodes_num/5)
        for index in range(self.AN_nodes_num):
            self.AN[index].degree = an_degree[index]
        # 第四步, 让 H 完成度的分配连接(如果第五步在第四步之后, 那么AN中的度已经消耗完毕, H剩余的度只能内部消化, 这种会出现为空的情况, 所以先H再AN
        # 内部消化有一个问题, 轮到最后几个节点, 会出现 当前节点虽然有度, 但是没有合适的邻接点了.

        for node in self.AN:
            AN_nei_candidate_list = reloadANinnerNeighbor(self, node)
            try:
                cur_node_num = 3
                if node.degree<cur_node_num:
                    continue
                while(cur_node_num):
                    rangeJ = random.randint(0, len(AN_nei_candidate_list)-1)
                    nodeN = AN_nei_candidate_list[rangeJ]
                    # 重新 找一个合适的邻居
                    while((nodeN.degree == 0) or nodeN.node_id in node.neighbors[nodeN.graph_id]):# 像G_AN_H的degree都是从-1开始的, 永远不可能是0, 因为要一直减
                        AN_nei_candidate_list.remove(nodeN)
                        rangeJ = random.randint(0, len(AN_nei_candidate_list)-1)
                        nodeN = AN_nei_candidate_list[rangeJ]

                    if nodeN.graph_id == 0:
                        node.addNeighbor(0, nodeN.node_id)
                        nodeN.addNeighbor(1, node.node_id)
                        self.H_all_degree-=1
                    if nodeN.graph_id == 1:
                        node.addNeighbor(1, nodeN.node_id)
                        nodeN.addNeighbor(1, node.node_id)
                        self.AN_all_degree-=1
                    if nodeN.graph_id == 2:
                        node.addNeighbor(2, nodeN.node_id)
                        nodeN.addNeighbor(1, node.node_id)
                    self.AN_all_degree-=1
                    node.degree -=1
                    cur_node_num -=1
                    nodeN.degree-=1
            except:
                pass
        # print("正在给H划分度")
        h_degree = distribute(degree_sum=self.H_all_degree, part_num=self.H_nodes_num, covariance=self.H_all_degree/self.H_nodes_num/5)
        for index in range(self.H_nodes_num):
            self.H[index].degree = h_degree[index]
        #print("正在让H中的节点寻找合适的邻居节点")
        for node in self.H:
            H_nei_candidate_list = reloadHneighbor(self, node)
            while(node.degree>0):
                rangeJ = random.randint(0, len(H_nei_candidate_list)-1)
                nodeN = H_nei_candidate_list[rangeJ]
                # 重新 找一个合适的邻居
                while((nodeN.degree == 0) or nodeN.node_id in node.neighbors[nodeN.graph_id]):# 像G_AN_H的degree都是从-1开始的, 永远不可能是0, 因为要一直减
                    H_nei_candidate_list.remove(nodeN)
                    rangeJ = random.randint(0, len(H_nei_candidate_list)-1)
                    nodeN = H_nei_candidate_list[rangeJ]

                if nodeN.graph_id == 0:
                    node.addNeighbor(0, nodeN.node_id)
                    nodeN.addNeighbor(0, node.node_id)
                    self.H_all_degree-=1
                if nodeN.graph_id == 1:
                    node.addNeighbor(1, nodeN.node_id)
                    nodeN.addNeighbor(0, node.node_id)
                    self.AN_all_degree-=1
                if nodeN.graph_id == 2:
                    node.addNeighbor(2, nodeN.node_id)
                    nodeN.addNeighbor(0, node.node_id)
                self.H_all_degree -=1
                node.degree -=1
                nodeN.degree-=1 #如果是G_H_H子图的节点, 这个degree减不减无所谓
        # 第五步, 基于节点分配的度, 找到合适的邻接点
        # 首先创建一个集合, 里面是所有有度的AN节点

        # print("正在为AN节点找合适的邻居")
        for node in self.AN:
            AN_nei_candidate_list = reloadANneighbor(self, node)
            try:
                while(node.degree):
                    rangeJ = random.randint(0, len(AN_nei_candidate_list)-1)
                    nodeN = AN_nei_candidate_list[rangeJ]
                    # 重新 找一个合适的邻居
                    while((nodeN.degree == 0) or nodeN.node_id in node.neighbors[nodeN.graph_id]):# 像G_AN_H的degree都是从-1开始的, 永远不可能是0, 因为要一直减
                        AN_nei_candidate_list.remove(nodeN)
                        rangeJ = random.randint(0, len(AN_nei_candidate_list)-1)
                        nodeN = AN_nei_candidate_list[rangeJ]

                    if nodeN.graph_id == 0:
                        node.addNeighbor(0, nodeN.node_id)
                        nodeN.addNeighbor(1, node.node_id)
                        self.H_all_degree-=1
                    if nodeN.graph_id == 1:
                        node.addNeighbor(1, nodeN.node_id)
                        nodeN.addNeighbor(1, node.node_id)
                        self.AN_all_degree-=1
                    if nodeN.graph_id == 2:
                        node.addNeighbor(2, nodeN.node_id)
                        nodeN.addNeighbor(1, node.node_id)
                    self.AN_all_degree-=1
                    node.degree -=1
                    nodeN.degree-=1 #如果是G_AN_H子图的节点, 这个degree减不减无所谓
            except:
                pass