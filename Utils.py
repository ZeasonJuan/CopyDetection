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
    for line in lines:
        print(line)
    # 对空行处理
    for i in range(len(lines)):
        if lines[i] == "":
            del lines[i]
    controllerGraph = {}
    controllerGraph[0] = [1]
    base_node = 0  # base_node,表示当前模块在起始模块开始的节点
    getGraph(lines, len(lines), base_node, controllerGraph, len(lines))
    print(controllerGraph)
    return controllerGraph


def getGraph(lines, node_num, base_node, controllerGraph, all_lines_num):
    special_logic = ['if', 'while', 'for']
    count = 1  # 当前模块中的偏移地址,第一行已经处理过
    while count < node_num:
        if lines[count].strip().split(" ")[0] in special_logic:  # 处理复杂逻辑
            # 生成子模块
            sub_lines, k = getSubLines(lines, node_num, count)
            # 逻辑处理
            solveSpecialLogic(sub_lines, base_node + count, lines[count].strip().split(" ")[0], controllerGraph,
                              all_lines_num)
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
    sub_lines = [lines[base_node]]
    head_space_number = getSpaceNumBefore(lines[base_node])
    k = 1
    # 生产子模块['if',"elif", "else", 'while' 'for','return']
    while (base_node + k) < node_num:
        if lines[base_node].strip().split(" ")[0] in ["for", "while"]:
            if getSpaceNumBefore(lines[base_node + k]) > head_space_number:
                sub_lines.append(lines[base_node + k])
                k = k + 1
            else:
                break
        else:  # if模块
            while base_node + k < node_num:
                if getSpaceNumBefore(lines[base_node + k]) > head_space_number:
                    sub_lines.append(lines[base_node + k])
                    k = k + 1
                elif getSpaceNumBefore(lines[base_node + k]) == head_space_number:
                    if lines[base_node + k].strip().split(" ")[0] in ["else", "elif"]:
                        sub_lines.append(lines[base_node + k])
                        k = k + 1
                    else:
                        break
            break

    return sub_lines, k


def solveSpecialLogic(sub_lines, base_node, type, controllerGraph, all_lines_num):
    """
    paragm:sub_lines 进行处理的对象
           node 子模块在原模块中的位置
           len(sub_lines) 子模块的大小
           type 子模块的类型
           controllerGraph 处理结果，传址调用
    """
    special_logic = ['if', 'while', 'for']
    if type == special_logic[0]:
        print("solve if logic")
        head_space_num = getSpaceNumBefore(sub_lines[0])
        i = 1
        if_sub = []  # if-elif-else的标号
        while i < len(sub_lines):
            if getSpaceNumBefore(sub_lines[i]) > head_space_num:
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
                controllerGraph[base_node + k - 1] = [base_node + len(sub_lines)]
                getGraph(sub_lines[start:k], len(sub_lines[start:k]), base_node + start, controllerGraph, all_lines_num)
                start = k
            # 对最后一个else/elif处理
            set = [base_node + start + 1]  # if指向下一句
            set.append(base_node + len(sub_lines))
            controllerGraph[base_node + start] = set
            getGraph(sub_lines[start:], len(sub_lines[start:]), base_node + start, controllerGraph, all_lines_num)

    elif type == special_logic[1]:
        # TODO
        print("solve while logic")

        getGraph(sub_lines, len(sub_lines), base_node, controllerGraph, all_lines_num)
    elif type == special_logic[2]:
        # TODO
        print("for")
        getGraph(sub_lines, len(sub_lines), base_node, controllerGraph, all_lines_num)


def getSpaceNumBefore(line):
    c = re.match(r'^( *?)[a-z0-9A-Z]', line)
    if c is None:
        # print(line)
        return 0
    return len(c.group()) - 1
