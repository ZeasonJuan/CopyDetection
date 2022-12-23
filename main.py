import random

from Reader import Reader
from Utils import generateControllerGraph
from superRe import superRe

if __name__ == "__main__":
     reader = Reader("C:\\Users\\19237\\PycharmProjects\\AllHomeWorkInThis\\SoftwareTesting")
     file_list = reader.getFileList()
     method_list = reader.get_fd()
     print(method_list.get(file_list[3])[2])
     print(generateControllerGraph(method_list.get(file_list[3])[2]))


