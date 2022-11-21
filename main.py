from Reader import Reader
from Utils import generateControllerGraph
from superRe import superRe

if __name__ == "__main__":
    reader = Reader("D:\\Python_Code\\pythonProject\\alien_invasion")
    file_list = reader.getFileList()
    method_list = reader.get_fd()
    generateControllerGraph(method_list.get(file_list[3])[16])

