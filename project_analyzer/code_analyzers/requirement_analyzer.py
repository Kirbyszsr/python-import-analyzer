from contrib.structs.file import File
from contrib.structs.requirementFile import RequirementFile
from contrib.elements.codeblock import Class, Method, Variate, Import
from project_analyzer.code_analyzers.analyzer import Analyzer

import re


class RequirementAnalyzer(Analyzer):

    def __init__(self, code_file):
        super(RequirementAnalyzer, self).__init__(code_file)
        # self.row = 0
        # 当前阅读的行数数据
        # self.rows = []
        self.current_line = 0

    def read_file(self):
        """
        读取文件的内容
        :return: 一个list, 包含该文件的所有row
        """
        # 获取url
        code_file_url = self.code_file.get_concrete_url(base_url='')
        try:
            f = open(code_file_url, encoding='utf-8', mode='r')
            f_lines = f.readlines()
        finally:
            if f:
                f.close()
        return f_lines if f_lines else []

    def parse_lines(self):
        """
        :param line:
        :return:

        先行对line中可能出现的单行注释或者多行注释
        进行去注释操作
        """
        new_rows = []
        for raw_line in self.rows:
            new_line = re.sub(r'#.*$', "", raw_line)
            new_rows.append(new_line)
        self.rows = new_rows
        return

    def read_line(self):
        """
        :param self:
        :param row:
        :return: 一行处理过后的代码数据; 读取本行所占用的行数
        当前行指针向下移动若干行,行数等于在处理过程中阅读的行数

        * 如果有注释数据，则略过这些注释数据
        """
        if self.current_line < len(self.rows):
            row = self.rows[self.current_line]
            self.current_line += 1
            return row, 1
        else:
            return None, 0

    def next_line(self):
        """
        :return: 下一行代码数据。
        当前行指针不移动。
        """

        return self.rows[self.current_line +
                         1] if self.current_line + 1 < len(self.rows) else None

    def parse_class(self, line, name):
        """
        创建并返回一个内含对象为空的class对象
        :param line: 所在行数
        :param name: 对象名
        :return: Class
        """
        return NotImplemented

    def parse_method(self, line, name):
        """
        创建并返回一个内含对象为空的method对象
        :param line: 所在行数
        :param name: 对象名
        :return: Method
        """
        return NotImplemented

    def parse_variate(self, line, name):
        """
        创建并返回一个内含对象为空的variate对象
        :param line: 所在行数
        :param name: 变量名
        :return: Method
        """
        return NotImplemented

    def parse_import(
            self,
            line,
            arg_from,
            arg_import,
            arg_as,
            arg_version='*'):
        """
         创建并返回一个内含对象为空的import对象
        :param line: 所在行数
        :param arg_from:  from参数
        :param arg_import: import参数
        :param arg_as: as参数
        :param arg_version: import的包的version
        :return: Import
        """
        if not arg_from:
            # import * [as *]
            return Import(name=arg_import,
                          filename=self.code_file.filename,
                          line=line,
                          from_element=arg_import,
                          import_element='*',
                          as_element=arg_as,
                          version=arg_version)
        else:
            # from * import * [as *]
            return Import(name=arg_from,
                          filename=self.code_file.filename,
                          line=line,
                          from_element=arg_from,
                          import_element=arg_import,
                          as_element=arg_as,
                          version=arg_version)

    def analyze(self):
        """
        :param self:
        :param code_file: 一个经过file_analyzer处理过的File对象，它的类型是文件
        :return: 一个CodeFile或RequirementFile对象(或JavaCodeFile对象)，
                 具体对象类型依据识别出的代码类型决定
                 基于原有File对象，同时包含Code的文件信息
        """
        if not isinstance(self.code_file, File):
            raise TypeError(
                '代码的分析对象必须是一个contrib.structs.File对象,而对象的类型是' + str(type(self.code_file)))
        if self.code_file.file_type is not "file":
            raise TypeError('代码的分析对象必须是一个文件,而对象是一个' + self.code_file.file_type)

        requirement_file = RequirementFile(filename=self.code_file.filename,
                                           owned_by=None)

        self.rows = self.read_file()
        self.parse_lines()
        imports = []
        while True:
            line, read_line_count = self.read_line()
            if read_line_count == 0:
                break
            elements = re.findall(
                "([a-zA-z0-9.]+)([!><=].*[0-9].*)", string=line)
            imports.append(elements)
            for element in elements:
                requirement_file.add_element(
                    self.parse_import(
                        line=self.current_line,
                        arg_from=element[0],
                        arg_import='*',
                        arg_as=elements[0],
                        arg_version=element[1].strip()))
            # imports.append(self.parse_import(self.current_line,))
        return requirement_file


if __name__ == "__main__":
    file_url = 'E:\\工作\\华为云项目\\keystone\\requirements.txt'

    sample_requirement_file = File(file_url)
    analyzer = RequirementAnalyzer(sample_requirement_file)

    require_file = analyzer.analyze()
    print('imports:')
    print(require_file.imports())
