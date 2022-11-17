import os.path as op
import os

class Reader:
    def __init__(self, file_direct):
        self.file_direct = file_direct
        self.file_direct += "\\src"

        self.file_list = self.haveFileList([])
        self.file_java_string = self.havaJavaFileString()

    def haveFileList(self, new_file_list):
        for home, dirs, files in os.walk(self.file_direct):
            for filename in files:
                if filename.endswith(".java"):
                    new_file_list.append(op.join(home, filename))

        return  new_file_list

    def getFileList(self):
        return self.file_list

    def havaJavaFileString(self):
        aDict = {}
        for i in range(len(self.file_list)):
            this_file = self.file_list[i]
            with open(this_file, "r", encoding="utf-8") as f:
                aDict[this_file] = f.read()
        return aDict

    def getJavaFileString(self):
        return self.file_java_string


if __name__ == "__main__":
    have_a_test = Reader("D:\java文件\idea\IdeaCode\RJQXAnalyzation")
    file_string = have_a_test.getJavaFileString()
    print(file_string.keys())
