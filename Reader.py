import os.path as op
import os

class Reader:
    def __init__(self, file_direct):
        self.file_direct = file_direct
        self.file_direct += "\\src"

        self.file_list = self.haveFileList([])
        self.file_java_string = self.havaJavaFileString()
        self.java_method = self.findMethod()

    def haveFileList(self, new_file_list):
        """
        :param new_file_list:
        :return: list['filename']
        """
        for home, dirs, files in os.walk(self.file_direct):
            for filename in files:
                if filename.endswith(".java"):
                    new_file_list.append(op.join(home, filename))

        return new_file_list

    def havaJavaFileString(self):
        """
        :return: Dict{'fileName':'context'}
        """
        aDict = {}
        for i in range(len(self.file_list)):
            this_file = self.file_list[i]
            with open(this_file, "r", encoding="utf-8") as f:
                aDict[this_file] = f.read()
        return aDict

    def findMethod(self):
        """
        :return:Dict{"methodName":"context"}
        """
        methodDict = {}
        for i in self.file_java_string.keys():
            context = self.file_java_string.get(i)
            """TODO"""
        return methodDict

    def getFileList(self):
        return self.file_list

    def getJavaFileString(self):
        return self.file_java_string

    def getJavaMethod(self):
        return self.java_method


if __name__ == "__main__":
    have_a_test = Reader("D:\java文件\idea\IdeaCode\RJQXAnalyzation")
    have_a_test.findClass()
