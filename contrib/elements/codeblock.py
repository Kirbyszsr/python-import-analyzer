# Codeblock.py
# 定义静态代码元素


class CodeElement(object):
    """
    代码元素通用属性
    """
    def __init__(self, type, filename, line):
        # 代码元素所在种类名
        self.type = type
        # 代码元素所在文件名
        self.filename = filename
        # 代码元素所在文件行数
        self.line = line
        pass


class Class(CodeElement):
    """
    函数类对象
    """
    pass


class Method(CodeElement):
    """
    函数方法类对象
    """
    pass


class Variate(CodeElement):
    """
    变量对象
    """
    pass

class Import(CodeElement):
    """
    外部调用语句对象
    """
    pass