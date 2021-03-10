import os
from contrib.structs.file import File
from contrib.structs.codefile import CodeFile
from contrib.elements.codeblock import CodeElement, Class, Method, Variate, Import
from project_analyzer.code_analyzers.analyzer import Analyzer


class PythonAnalyzer(Analyzer):

    def __init__(self,code_file):
        super(PythonAnalyzer,self).__init__(code_file)

    def parse_class(self, line, name):
        return Class(name=name,
                     filename=self.code_file.filename,
                     line=line,
                     owns=[])

    def parse_method(self, line, name):
        return Method(name=name,
                      filename=self.code_file.filename,
                      line=line,
                      owns=[])

    def parse_variate(self, line, name):
        return Variate(name=name,
                       filename=self.code_file.filename,
                       line=line)

    def parse_import(self, line, arg_import, arg_as=None, arg_from=None, arg_version='*'):
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
        if type(self.code_file) is not File:
            raise TypeError('代码的分析对象必须是一个contrib.structs.File对象,而对象的类型是' + type(self.code_file))
        if self.code_file.file_type is not "file":
            raise TypeError('代码的分析对象必须是一个文件,而对象是一个' + self.code_file.file_type)
        code_file = CodeFile(filename=self.code_file.filename,
                             owned_by=None)
        code_file.code_type = 'python'

        
        return code_file

    def read_line(self):
        """
        :param self:
        :param row:
        :return: 一行处理过后的代码数据; 读取本行所占用的行数
        当前行指针向下移动若干行,行数等于在处理过程中阅读的行数

        * 如果有注释数据，则略过这些注释数据
        """
        return None

    def next_line(self):
        return None
