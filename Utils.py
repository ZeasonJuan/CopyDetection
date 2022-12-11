import re


def generateControllerGraph(method):
    """
    param: method 方法 String类型
    return：method对应的controllerGraph
    """
    if method is None:
        return {}
    # 将方法划分成行
    lines = method.split("\n")
    # for line in lines:
    #     print(line)
    # 对空行处理
    for i in range(len(lines)):
        if lines[i] == "":
            del lines[i]
    nums = len(lines)
    for i in range(nums):
        if lines[i].strip().split(" ")[0] in ["for", "while"]:
            k = 1
            while i+k < nums:
                if getSpaceNumBefore(lines[i + k]) > getSpaceNumBefore(lines[i]):
                    k = k + 1
                    if i + k == nums:
                        lines.insert(i + k, " ")
                else:
                    lines.insert(i+k, " ")
                    break
    controllerGraph = {}
    controllerGraph[0] = [1]
    base_node = 0  # base_node,表示当前模块在起始模块开始的节点
    getGraph(lines, len(lines), base_node, controllerGraph, len(lines))
    controllerGraph = sorted(controllerGraph.items(), key=lambda x:x[0])
    print(controllerGraph)
    return controllerGraph


def getGraph(lines, node_num, base_node, controllerGraph, all_lines_num):
    # """
    # brief :动态生成图controllerGraph
    # param :lines 方法模块（if、for、while)对应的列表，元素为方法的一行
    #        node_num lines的行数
    #        base_node lines第一行在原始方法里的行号
    #        controllerGraph 动态生成图
    #        all_lines_num 总的行数
    # return：none
    # """
    special_logic = ['if', 'while', 'for']
    count = 1  # 当前模块中的偏移地址,第一行已经处理过
    while count < node_num:
        if lines[count].strip().split(" ")[0] in special_logic:  # 处理复杂逻辑
            # 生成子模块
            sub_lines, k = getSubLines(lines, node_num, count)
            # 逻辑处理
            solveSpecialLogic(sub_lines, base_node + count, lines[count].strip().split(" ")[0], controllerGraph,all_lines_num)
            count = count + k
        elif lines[count].strip().split(" ")[0] == "return":
            set = [all_lines_num]
            controllerGraph[base_node + count] = set
            count = count + 1
        else:  # 简单逻辑
            if base_node+count not in controllerGraph.keys():
                set = [base_node + count + 1]
                controllerGraph[base_node + count] = set
            count = count + 1


def getSubLines(lines, node_num, base_node):
    # """
    # brief:获取方法里的子模块(if-elif-else/for/while)
    # param :lines 方法模块对应的列表，元素为方法的一行
    #        node_num lines的行数
    #        base_node lines第一行在原始方法里的行号
    # return：子模块(if-elif-else/while/for)sub_lines
    # """
    sub_lines = [lines[base_node]]
    head_space_number = getSpaceNumBefore(lines[base_node])
    k = 1
    # 生产子模块['while' 'for']
    while (base_node + k) < node_num:
        if lines[base_node].strip().split(" ")[0] in ["for", "while"]:
            if getSpaceNumBefore(lines[base_node + k]) > head_space_number or lines[base_node+k] == " ":
                sub_lines.append(lines[base_node + k])
                k = k + 1
            else:
                break
        else:  # if模块
            while base_node + k < node_num:
                if getSpaceNumBefore(lines[base_node + k]) > head_space_number or lines[base_node+k] == " ":
                    sub_lines.append(lines[base_node + k])
                    k = k + 1
                elif getSpaceNumBefore(lines[base_node + k]) == head_space_number:
                    if lines[base_node + k].strip().split(" ")[0] in ["else", "elif", "else:"]:
                        sub_lines.append(lines[base_node + k])
                        k = k + 1
                    else:
                        break
                else:
                    break
            break

    return sub_lines, k


def solveSpecialLogic(sub_lines, base_node, type, controllerGraph, all_lines_num):
    # """
    # paragm:sub_lines 进行处理的对象
    #        base_node 子模块在原模块中的位置
    #        len(sub_lines) 子模块的大小
    #        type 子模块的类型
    #        controllerGraph 处理结果，传址调用
    # """
    special_logic = ['if', 'while', 'for']
    if type == special_logic[0]:
        print("solve if logic")
        head_space_num = getSpaceNumBefore(sub_lines[0])
        i = 1
        if_sub = []  # if-elif-else的标号
        # TODO deal with bug as followed
        while i < len(sub_lines):
            if getSpaceNumBefore(sub_lines[i]) > head_space_num or sub_lines[i] == " ":
                i = i + 1
            else:
                if_sub.append(i)
                i = i + 1
        # 处理框架
        if if_sub is None:  # 只有if语句
            set = [base_node + 1]  # if指向下一句
            set.append(base_node + len(sub_lines))  # 指向下一个模块
            controllerGraph[base_node] = set
            getGraph(sub_lines, len(sub_lines), base_node, controllerGraph, all_lines_num)
        else:  # 有elif\else
            start = 0
            for k in if_sub:
                set = [base_node + start + 1]  # if指向下一句
                set.append(base_node + k)
                controllerGraph[base_node + start] = set
                if base_node + k -1 not in controllerGraph.keys():
                    controllerGraph[base_node + k - 1] = [base_node + len(sub_lines)]
                getGraph(sub_lines[start:k], len(sub_lines[start:k]), base_node + start, controllerGraph, all_lines_num)
                start = k
            # 对最后一个else/elif处理
            set = [base_node + start + 1]  # if指向下一句
            set.append(base_node + len(sub_lines))
            controllerGraph[base_node + start] = set
            getGraph(sub_lines[start:], len(sub_lines[start:]), base_node + start, controllerGraph, all_lines_num)

    elif type == special_logic[1]:
        print("solve while logic")
        set = [base_node+1]  # 指向while的下一句
        set.append(base_node+len(sub_lines))  # 指向下一个模块
        controllerGraph[base_node] = set
        i = 1
        continue_sub = []  # continue标号
        break_sub = []
        while i < len(sub_lines):
            if sub_lines[i].strip().split(" ")[0] == "continue":
                continue_sub.append(i)
            if sub_lines[i].strip().split(" ")[0] == "break":
                break_sub.append(i)
            i = i + 1
        controllerGraph[base_node+len(sub_lines)-1] = [base_node]
        for continue_s in continue_sub:
            controllerGraph[base_node+continue_s] = [base_node]
        for break_s in break_sub:
            controllerGraph[base_node+break_s] = [base_node+len(sub_lines)]
        getGraph(sub_lines[:-1], len(sub_lines[:-1]), base_node, controllerGraph, all_lines_num)
    elif type == special_logic[2]:
        print("solve for logic")
        set = [base_node + 1]  # 指向for的下一句
        set.append(base_node + len(sub_lines))  # 指向下一个模块
        controllerGraph[base_node] = set
        i = 1
        continue_sub = []  # continue标号
        break_sub = []
        while i < len(sub_lines):
            if sub_lines[i].strip().split(" ")[0] == "continue":
                continue_sub.append(i)
            if sub_lines[i].strip().split(" ")[0] == "break":
                break_sub.append(i)
            i = i + 1
        controllerGraph[base_node + len(sub_lines) - 1] = [base_node]
        for continue_s in continue_sub:
            controllerGraph[base_node + continue_s] = [base_node]
        for break_s in break_sub:
            controllerGraph[base_node + break_s] = [base_node + len(sub_lines)]
        getGraph(sub_lines[:-1], len(sub_lines[:-1]), base_node, controllerGraph, all_lines_num)


def getSpaceNumBefore(line):
    """
    brief:获取每一行的缩进格数
    param:line 一行代码
    return：line对应的缩进空格数
    """
    c = re.match(r'^( *?)[a-z0-9A-Z]', line)
    if c is None:
        # print(line)
        return 0
    return len(c.group()) - 1
