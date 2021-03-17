import abc
# from contrib.structs.codefile import CodeFile
# from contrib.elements.codeblock import CodeElement, Class, Method, Variate, Import


# 抽象代码分析器类
class Analyzer:

    def __init__(self, code_file):
        # 标记当前所使用的file
        self.code_file = code_file
        # 标记当前阅读行数
        self.row = 0
        # 当前阅读的行数数据
        self.rows = []

    @abc.abstractmethod
    def read_file(self):
        """
        读取文件的内容
        :return: 一个list, 包含该文件的所有row
        """
        return NotImplemented

    @abc.abstractmethod
    def read_line(self):
        """
        :param self:
        :param row:
        :return: 一行处理过后的代码数据; 读取本行所占用的行数
        当前行指针向下移动若干行,行数等于在处理过程中阅读的行数

        * 如果有注释数据，则略过这些注释数据
        """
        return NotImplemented, NotImplemented

    @abc.abstractmethod
    def next_line(self):
        """
        :return: 下一行代码数据。
        当前行指针不移动。
        """
        return NotImplemented

    @abc.abstractmethod
    def parse_class(self, line, name):
        """
        创建并返回一个内含对象为空的class对象
        :param line: 所在行数
        :param name: 对象名
        :return: Class
        """
        return NotImplemented

    @abc.abstractmethod
    def parse_method(self, line, name):
        """
        创建并返回一个内含对象为空的method对象
        :param line: 所在行数
        :param name: 对象名
        :return: Method
        """
        return NotImplemented

    @abc.abstractmethod
    def parse_variate(self, line, name):
        """
        创建并返回一个内含对象为空的variate对象
        :param line: 所在行数
        :param name: 变量名
        :return: Method
        """
        return NotImplemented

    @abc.abstractmethod
    def parse_import(self, line, arg_from, arg_import, arg_as, arg_version='*'):
        """
         创建并返回一个内含对象为空的import对象
        :param line: 所在行数
        :param arg_from:  from参数
        :param arg_import: import参数
        :param arg_as: as参数
        :param arg_version: import的包的version
        :return: Import
        """
        return NotImplemented

    @abc.abstractmethod
    def analyze(self):
        """

        :param self:
        :param code_file: 一个经过file_analyzer处理过的File对象，它的类型是文件
        :return: 一个CodeFile或RequirementFile对象(或JavaCodeFile对象)，
                 具体对象类型依据识别出的代码类型决定
                 基于原有File对象，同时包含Code的文件信息
        """
        return NotImplemented