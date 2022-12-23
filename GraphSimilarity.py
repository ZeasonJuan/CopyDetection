import random

from Reader import Reader
from Utils import generateControllerGraph
from wwl import wwl
import matplotlib.pyplot as plt
import igraph as ig
import numpy as np
print("只能测试python项目")
reader_directory1 = input('请输入项目1文件夹路径')
reader_directory2 = input('请输入项目2文件夹路径')


reader1 = Reader(reader_directory1)
reader2 = Reader(reader_directory2)


file_list1 = reader1.getFileList()
file_list2 = reader2.getFileList()
method_list1 = reader1.get_fd()
method_list2 = reader2.get_fd()



every_max_similarity = []

for i in range(len(file_list1)):
    file_to_file_similarity = 0
    for j in range(len(file_list2)):
        the_one_to_one = []
        for k in range(len(method_list1.get(file_list1[i]))):
            temp = 0
            for z in range(len(method_list2.get(file_list2[j]))):
                jianlong_graph = generateControllerGraph(method_list1.get(file_list1[i])[k])
                jianlong_graph1 = generateControllerGraph(method_list2.get(file_list2[j])[z])
                g = ig.Graph()
                g1 = ig.Graph()

                g.add_vertices(len(jianlong_graph) + 1)
                g1.add_vertices(len(jianlong_graph1) + 1)
                for a in range(len(jianlong_graph)):
                    for b in range(len(jianlong_graph[a][1])):
                        g.add_edge(jianlong_graph[a][0], jianlong_graph[a][1][b])

                for a in range(len(jianlong_graph1)):
                    for b in range(len(jianlong_graph1[a][1])):
                        g1.add_edge(jianlong_graph1[a][0], jianlong_graph1[a][1][b])

                ss = np.array([g, g1], dtype=object)
                temp = max(wwl(ss, num_iterations=5)[0][1], temp)
            the_one_to_one.append(temp)
        file_to_file_similarity = max(sum(the_one_to_one) / len(the_one_to_one), file_to_file_similarity) if len(the_one_to_one) != 0 else 0.5567
    every_max_similarity.append(file_to_file_similarity)
print("两个项目的总体相似度为", sum(every_max_similarity) / len(every_max_similarity))



# reader = Reader("C:\\Users\\19237\\PycharmProjects\\AllHomeWorkInThis\\SoftwareTesting")
# file_list = reader.getFileList()
# method_list = reader.get_fd()
# aa = reader.getJavaFileString()
# print(file_list[1])
# print(aa.get(file_list[1]))
# jianlong_graph = generateControllerGraph(method_list.get(file_list[3])[2])
# jianlong_graph1 = generateControllerGraph(method_list.get(file_list[3])[1])
# g = ig.Graph()
# g1 = ig.Graph()
#
# g.add_vertices(len(jianlong_graph) + 1)
# g1.add_vertices(len(jianlong_graph1) + 1)
#
# for i in range(len(jianlong_graph)):
#     for j in range(len(jianlong_graph[i][1])):
#         g.add_edge(jianlong_graph[i][0], jianlong_graph[i][1][j])
#
# for i in range(len(jianlong_graph1)):
#     for j in range(len(jianlong_graph1[i][1])):
#         g1.add_edge(jianlong_graph1[i][0], jianlong_graph1[i][1][j])
# ss = np.array([g, g1], dtype=object)
# print(wwl(ss, num_iterations=5)[0][1])


