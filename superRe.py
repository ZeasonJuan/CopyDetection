import re

class superRe:
    def __init__(self, aString):
        self.string_to_be_processed = aString.split("\n")
        while '' in self.string_to_be_processed:
            self.string_to_be_processed.remove('')

        self.str_can_be_solved = ['for', 'while', 'def', 'if', 'elif', 'else']

    #封装了一个类，返回值是一个列表，列表里装了字符串（该关键符号的模块）输入是你想要的模块比如for里面的if里面的什么什么的
    def getAllIntern(self, astr):
        whole_string_list = self.string_to_be_processed
        if astr not in self.str_can_be_solved:
            return []
        final_list = []
        temp = ''
        is_in_the_realm = False
        indent_number = 0
        for i in range(len(whole_string_list)):
            this_line = whole_string_list[i]
            if not is_in_the_realm and astr not in this_line:
                continue
            if astr in this_line and self.ishead(astr, this_line):
                final_list.append(temp)
                temp = ''

                indent_number = self.how_many_space_before(this_line)
                is_in_the_realm = True
                temp += this_line+'\n'
                continue

            if self.how_many_space_before(this_line) <= indent_number:
                final_list.append(temp)
                temp = ''
                is_in_the_realm = False
                continue

            temp += this_line+'\n'

        while '' in final_list:
            final_list.remove('')
        return final_list



    def how_many_space_before(self, line):
        c = re.match(r'^( *?)[a-z0-9A-Z]', line)
        return len(c.group())-1

    def ishead(self, astr, line):
        pettern = re.compile(r'^( *?)'+astr)
        a = re.match(pettern, line)
        if a is None:
            return False
        return True



if __name__ == "__main__":
    file_str = ''
    with open("C:\\Users\\19237\\PycharmProjects\\AllHomeWorkInThis\\resource\\totest.txt", "r", encoding="utf-8") as f:
        file_str = f.read()

    ast = superRe(file_str)
    print(superRe.getAllIntern(ast, 'def'))



