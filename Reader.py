import os.path as op
import os
import re
from superRe import superRe


class Reader:
    def __init__(self, file_direct):
        self.file_direct = file_direct

        self.file_list = self.haveFileList([])
        self.file_java_string = self.havaJavaFileString()
        self.file_dict_which_key_is_path_And_value_is_list_that_has_all_method_separated = self.makeEveryMethod()

    def haveFileList(self, new_file_list):
        """
        :param new_file_list:
        :return: list['filename']
        """
        for home, dirs, files in os.walk(self.file_direct):
            for filename in files:
                if filename.endswith(".py"):
                    new_file_list.append(op.join(home, filename))

        return new_file_list

    def get_fd(self):
        return self.file_dict_which_key_is_path_And_value_is_list_that_has_all_method_separated

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

    def getFileList(self):
        return self.file_list

    def getJavaFileString(self):
        return self.file_java_string


    # 得到所有方法
    def makeEveryMethod(self):
        # 新建一个字典，该字典的key为文件，value为列表，列表中装了n个元组，每个元组对应了一个方法
        a_new_dict = {}
        for key in self.file_java_string:
            a_new_dict[key] = []
        '''    
        whole_string_dict = self.file_java_string
    
        for key in self.file_java_string:
            re.findall(r'def (.*?):(.*?((?=\ndef)|(?=\n[a-z0-9A-Z])|(?= def)))', whole_string_dict[key], re.S)
        '''
        for key in self.file_java_string:
            ast = superRe(self.file_java_string[key])
            a_new_dict[key] = ast.getAllIntern('def')
        return a_new_dict


if __name__ == "__main__":
    have_a_test = Reader("C:\\Users\\19237\\PycharmProjects\\AllHomeWorkInThis")
    file_string = have_a_test.getJavaFileString()
    the_py_i_want_to_test = ''
    for key in file_string.keys():
        if key.endswith('myFirstPytorch.py'):
            the_py_i_want_to_test = key
    string_of_this_file = file_string[the_py_i_want_to_test]

    the_list = re.findall(r'\n( *?)def', string_of_this_file, re.S)
    print(have_a_test.get_fd())
