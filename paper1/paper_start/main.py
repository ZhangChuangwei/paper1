# Writter: Shuhao Xu xsh20@mails.tsinghua.edu.cn
import numpy as np

# from Parameters import *
from Network1 import Network1
import pandas as pd
import time


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    times = 2
    times1 = 2
    para_list = []

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

    for parameters in para_list:
        # 暂时不使用 Network 网络
        # paraList = []
        # time_string1 = time.strftime("%Y-%m-%d-%H_%M_%S", time.localtime(time.time()))
        # for i in range(times):
        #     print("***********************************************************************************")
        #     print("第"+str(i)+"次 Net")
        #     network = Network(parameters)
        #     paraList.append(network.returnParameters())
        # names = ["H_score", "H_nodes", "H_goodnodes", "H_averageNodeDegree",
        #         "AN_nodes", "AN_goodDecGene", "AN_nodeEdge", "AN_averageDegree",
        #         "G_AN_H_nodes", "node_level", "H_connected_space"]
        # result = pd.DataFrame(columns=names, data=paraList)
        # scores = result['H_score']
        # net_ave = scores.mean()
        # net_max = scores.max()
        # net_min = scores.min()
        # net_med = scores.median()
        # net_std = scores.std()
        # result.loc[times+1] = {'H_score': ""}
        # result.loc[times+2] = {'H_score': "exp_times is: "+str(times)}
        # result.loc[times+3] = {'H_score': "ave_score is: "+str(net_ave)}
        # result.loc[times+4] = {'H_score': "max_score is: "+str(net_max)}
        # result.loc[times+5] = {'H_score': "min_score is: "+str(net_min)}
        # result.loc[times+6] = {'H_score': "median_score is: "+str(net_med)}
        # result.loc[times+7] = {'H_score': "std_score is: "+str(net_std)} #标准差
        # time_string = time.strftime("%Y-%m-%d-%H_%M_%S",time.localtime(time.time()))
        # excel_name = time_string+" Net Repeat "+str(times)+" times.csv"
        # result.to_csv("experiment_result\\"+excel_name)
        # print("***************************************************************************************")
        # print(time_string1)
        # print(time_string)
        # print("%d times' average score %f: "%(times, net_ave))
        # print("max score %f: " % (net_max))
        # print("min score %f: " % (net_min))
        # print("median score %f: " % (net_med))
        # print("std score %f: " % (net_std))

        paraList = []
        for i in range(times1):
            print("***********************************************************************************")
            print("第"+str(i)+"次 Net1")
            network = Network1(parameters)
            paraList.append(network.returnParameters())
        names = ["H_score", "H_nodes", "H_goodnodes", "H_averageNodeDegree",
                "AN_nodes", "AN_goodDecGene", "AN_nodeEdge", "AN_averageDegree",
                "G_AN_H_nodes", "node_level", "H_connected_space"]

        result1 = pd.DataFrame(columns=names, data=paraList)
        scores = result1['H_score']
        net_ave = scores.mean()
        net_max = scores.max()
        net_min = scores.min()
        net_med = scores.median()
        net_std = scores.std()
        result1.loc[times+1] = {'H_score': ""}
        result1.loc[times+2] = {'H_score': "exp_times is: "+str(times)}
        result1.loc[times+3] = {'H_score': "ave_score is: "+str(net_ave)}
        result1.loc[times+4] = {'H_score': "max_score is: "+str(net_max)}
        result1.loc[times+5] = {'H_score': "min_score is: "+str(net_min)}
        result1.loc[times+6] = {'H_score': "median_score is: "+str(net_med)}
        result1.loc[times+7] = {'H_score': "std_score is: "+str(net_std)} #标准差
        time_string = time.strftime("%Y-%m-%d-%H_%M_%S",time.localtime(time.time()))
        excel_name = time_string+" Net1 Repeat "+str(times)+" times.csv"
        result1.to_csv("experiment_result\\"+excel_name)

        print("***************************************************************************************")
        # print(time_string1)
        print(time_string)
        print("%d times' average score %f: "%(times, net_ave))
        print("max score %f: " % (net_max))
        print("min score %f: " % (net_min))
        print("median score %f: " % (net_med))
        print("std score %f: " % (net_std))

