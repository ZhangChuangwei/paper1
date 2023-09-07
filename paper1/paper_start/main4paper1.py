# 这个 main 是针对论文
# Global reliable diagnosis of networks based on Self-Comparative Diagnosis Model and g-good-neighbor property
# 设定的

import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import time
import pandas as pd
from Algorithm.paper1 import paper1

from network.network1 import Network1
from utils.get_para import return_para
from utils.pmcDecNet import PMC_decNet
from utils.calSelfTec import selfTec


if __name__ == '__main__':
    
    # 这里调整下参数设置就好
    para_list = []
    # 参数设置
    cur_net = Network1 #当前选择哪个网络
    times = 5 #每一个网络重复实验次数
    cur_algorithm = paper1   #当前选择哪个检测算法
    algo_return_H_num = 20 #当前算法要返回几个好的H点, 因为一个好点可能不太够用

    # 设置一下生成网络的参数
    test_or_not = True #正式跑的时候设置为 False, 设置为True是用来简单测试代码是否跑通.为True时, 会把网络的节点数目缩小, 以便于快速测试


    if test_or_not:
        H_nodes_num, H_good_num, H_degree, AN_nodes_num, AN_decGood_num, AN_degree_num, G_AN_H_nodes, Node_level, g_goodN \
        = 1000,     100,        50,         2000,           100,              50,        1000,           3,        25
        parameters_tmp = [[H_nodes_num, H_good_num, H_degree], [AN_nodes_num, AN_decGood_num, AN_degree_num],
                          [G_AN_H_nodes], [Node_level, g_goodN]]
        para_list.append(parameters_tmp)
        # Node level 指的是坏点有多少个度,好点的 node level 为 0, 坏点为 1,..,Node_level

    else:
        #第一组 变AN中诊断能力好的点
        H_nodes_num, H_good_num, H_degree, AN_nodes_num, AN_decGood_num, AN_degree_num, G_AN_H_nodes, Node_level, g_goodN \
            = 1000,     400,        50,         2000,           25,              50,        10000,           7,        25
        #每个 for 循环里面自己加变量的尝试
        for i in range(7):
            parameters_tmp = [[H_nodes_num, H_good_num, H_degree], [AN_nodes_num, AN_decGood_num + i*25, AN_degree_num],
                        [G_AN_H_nodes], [Node_level, g_goodN]]
            para_list.append(parameters_tmp)

        # 第二组 变H中好点占比
        H_nodes_num, H_good_num, H_degree, AN_nodes_num, AN_decGood_num, AN_degree_num, G_AN_H_nodes, Node_level, g_goodN \
            = 1000,     125,        50,         2000,           100,              50,        10000,          7,        25
        for i in range(7):
            parameters_tmp = [[H_nodes_num, H_good_num + i*125, H_degree], [AN_nodes_num, AN_decGood_num, AN_degree_num],
                            [G_AN_H_nodes], [Node_level, g_goodN]]
            para_list.append(parameters_tmp)

        # 第三组 变AN中的度
        H_nodes_num, H_good_num, H_degree, AN_nodes_num, AN_decGood_num, AN_degree_num, G_AN_H_nodes, Node_level, g_goodN \
            = 1000,     400,        50,         2000,           100,              20,        10000,           7,       25
        for i in range(7):
            parameters_tmp = [[H_nodes_num, H_good_num, H_degree], [AN_nodes_num, AN_decGood_num, AN_degree_num+i*10],
                            [G_AN_H_nodes], [Node_level, g_goodN]]
            para_list.append(parameters_tmp)

        # 第四组 变H中的度
        H_nodes_num, H_good_num, H_degree, AN_nodes_num, AN_decGood_num, AN_degree_num, G_AN_H_nodes, Node_level, g_goodN \
            = 1000,     400,        20,         2000,           100,            50,        10000,           7,        25
        for i in range(7):
            parameters_tmp = [[H_nodes_num, H_good_num, H_degree+i*10], [AN_nodes_num, AN_decGood_num, AN_degree_num],
                            [G_AN_H_nodes], [Node_level, g_goodN]]
            para_list.append(parameters_tmp)

        # 第五组 变g_goodN
        H_nodes_num, H_good_num, H_degree, AN_nodes_num, AN_decGood_num, AN_degree_num, G_AN_H_nodes, Node_level, g_goodN \
            = 1000,     400,        50,         2000,           100,              50,        10000,           7,        10
        for i in range(7):
            parameters_tmp = [[H_nodes_num, H_good_num, H_degree], [AN_nodes_num, AN_decGood_num, AN_degree_num],
                            [G_AN_H_nodes], [Node_level, g_goodN+i*5]]
            para_list.append(parameters_tmp)

    # 按流程走整个过程
    for parameters in para_list:
        # 每一组参数保留一个csv文件
        paraList = []
        time_string = time.strftime("%Y-%m-%d-%H_%M_%S", time.localtime(time.time()))
        for i in range(times):
            print("***********************************************************************************")
            print("第"+str(i)+"次 Net")
            # start 核心运行模块! 
            network = cur_net(parameters) #生成网络, 到这里仅生成网络, 不进行检测
            # network = selfTec(network, p2_algo3, network.Node_level)
            good_H_list = cur_algorithm(network, algo_return_H_num, network.Node_level) #一个 list, 一般网络的标配是用新算法检测出好的 H 点, 然后用 PMC 在 H 中内部传播
            network = PMC_decNet(network, good_H_list) #用 PMC 算法通过已经检测出来的点, 检测H 内部的网络
            net_para = return_para(network)#返回一些检测的参数
            paraList.append(net_para)
            # end 核心运行模块!     

        names = ["H_score", "H_connected_space", "accuracy", "precision", "recall", "H_nodes", "H_goodnodes", "H_averageNodeDegree",
                "AN_nodes", "AN_goodDecGene", "AN_nodeEdge", "AN_averageDegree",
                "G_AN_H_nodes", "node_level"]
        result = pd.DataFrame(columns=names, data=paraList)
        scores = result['H_score'] #这里的 H_score 是检测率的意思;
        net_ave = scores.mean()
        net_max = scores.max()
        net_min = scores.min()
        net_med = scores.median()
        net_std = scores.std()

        accuracy_score = result['accuracy']
        acc_ave = accuracy_score.mean()
        acc_max = accuracy_score.max()
        acc_min = accuracy_score.min()
        acc_med = accuracy_score.median()


        H_c_s = result['H_connected_space'].mean()
        result.loc[times+1] = {'H_score': ""} #这里 times+1 是在最后补充上统计数据, 每一个参数有一个统计数据
        result.loc[times+2] = {'H_score': "exp_times is: "+str(times)}
        result.loc[times+3] = {'H_score': "ave_score is: "+str(net_ave)}
        result.loc[times+4] = {'H_score': "max_score is: "+str(net_max)}
        result.loc[times+5] = {'H_score': "min_score is: "+str(net_min)}
        result.loc[times+6] = {'H_score': "median_score is: "+str(net_med)}
        result.loc[times+7] = {'H_score': "std_score is: "+str(net_std)} #标准差
        result.loc[times+8] = {'H_score': "ave_connected_space is: "+str(H_c_s)} #连通度的均值
        result.loc[times+9] = {'H_score': "ave_accuracy is: "+str(acc_ave)}
        result.loc[times+10] = {'H_score': "max_accuracy is: "+str(acc_max)}
        result.loc[times+11] = {'H_score': "min_accuracy is: "+str(acc_min)}
        result.loc[times+12] = {'H_score': "median_accuracy is: "+str(acc_med)}

        time_string1 = time.strftime("%Y-%m-%d-%H_%M_%S",time.localtime(time.time()))
        excel_name = time_string1+" Net Repeat "+str(times)+" times.xlsx"
        script_path = os.path.dirname(os.path.abspath(__file__))
        save_path = os.path.join(script_path, '..', 'experiment_result', excel_name)
        result.to_excel(save_path)
        print("***********************************************************************************")
        print('----------------------- The final result of the statistics. -----------------------')
        print("***********************************************************************************")
        print("%d times' average dec score: %f "%(times, net_ave)) 
        print(f"max score {net_max:.6f} \
                min score {net_min:.6f} ")
        print(f"median score {net_med:.6f} \
                std score {net_std:.6f} ")
        print(f"average accuracy: {acc_ave:.6f} ")
        print(f"max accuracy: {acc_max:.6f} \
                min accuracy: {acc_min:.6f} ")
        print(f"median accuracy: {acc_med:.6f} ")
