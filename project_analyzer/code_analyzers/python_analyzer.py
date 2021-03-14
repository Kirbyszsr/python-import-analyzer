from contrib.structs.file import File
from contrib.structs.codefile import CodeFile
from contrib.elements.codeblock import Class, Method, Variate, Import
from project_analyzer.code_analyzers.analyzer import Analyzer

# 正则表达式
import re
import abc as test
from py_compile import main as ce


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
        # 检查分析对象是否为一个File对象，且对应一个文件系统里的文件
        if type(self.code_file) is not File:
            raise TypeError('代码的分析对象必须是一个contrib.structs.File对象,而对象的类型是' + type(self.code_file))
        if self.code_file.file_type is not "file":
            raise TypeError('代码的分析对象必须是一个文件,而对象是一个' + self.code_file.file_type)

        # 创建一个CodeFile对象以返回
        code_file = CodeFile(filename=self.code_file.filename,
                             owned_by=None)
        code_file.code_type = 'python'

        code_lines = self.read_file()

        return code_file

    def read_file(self):
        """
        读取文件的内容
        :return: 一个list, 包含该文件的所有row
        """
        #获取url
        code_file_url = self.code_file.get_concrete_url(base_url='')
        try:
            f = open(code_file_url, encoding='utf-8', mode='r')
            f_lines = f.readlines()
        finally:
            if f:
                file.close()
        return f_lines if f_lines else []

    def read_line(self):
        """
        :param self:
        :param row:
        :return: 一行处理过后的代码数据; 读取本行所占用的行数
        当前行指针向下移动若干行,行数等于在处理过程中阅读的行数

        * 如果有注释数据，则略过这些注释数据
        """
        return None

    def parse_line(self, line):
        """
        :param line:
        :return:
        """
        """
        in_multiple_note = False
        multiple_note_flag = None
        for line in lines:
            if in_multiple_note and line.find(multiple_note_flag) == -1:
                continue
            elif in_multiple_note:
                in_multiple_note = False
                line = line[:line.find(multiple_note_flag)]
                multiple_note_flag = None
        """
        return None

    def next_line(self):
        return None


if __name__ == "__main__":
    file_url = "E:\\Works\\python-import-analyzer\\project_analyzer\\code_analyzers\\python_analyzer.py"
    try:
        file = open(file_url,encoding='utf-8',mode='r')
        lines = file.readlines()
    finally:
        if file:
            file.close()
        if not lines:
            lines = []

    code_file = CodeFile(file_url)
    analyzer = PythonAnalyzer(code_file)

    import_line = []
    def_line = []
    class_line = []
    equal_line = []

    for line in lines:
        code_line = re.sub(r'#.*$', "", line)
        code_line = re.sub(r'\'.*\'', '\'\'', code_line)
        code_line = re.sub(r'\".*\"', '\"\"', code_line)
        # if re.findall('import ?', line):
        if re.findall(r'(?:^|\s)import\s', code_line):
            import_line.append(code_line)
        if re.findall(r'(?:^|\s)def\s', code_line):
            def_line.append(code_line)
        if re.findall(r'(?:^|\s)class\s', code_line):
            class_line.append(code_line)
        if re.findall(r'\s=\s', code_line):
            equal_line.append(code_line)
    print(import_line)
    # print(def_line)
    # print(class_line)
    # print(equal_line)

    # 要使用;对同一行语句进行切块

    for line in import_line:
        elements = re.findall("from\s+(.+)\s+import\s+(.+)\s+as\s+(.+)",line)
        if elements != []:
            print(elements)
            print("MATCH SUCCEED(fia)")
            for element in elements:
                code_file.add_element(analyzer.parse_import(-1, arg_from=element[0], arg_import=element[1], arg_as=element[2]))
            continue

        elements = re.findall("from\s+(.+)\s+import\s+(.+)",line)
        if elements != []:
            print(elements)
            print("MATCH SUCCEED(fi)")
            for element in elements:
                code_file.add_element(analyzer.parse_import(-1, arg_from=element[0], arg_import=element[1]))
            continue

        elements = re.findall("import\s+(.+)as\s+(.+?)",line)
        if elements != []:
            print(elements)
            print("MATCH SUCCEED(ia)")
            for element in elements:
                code_file.add_element(analyzer.parse_import(-1, arg_from=element[0], arg_import=element[1]))
            continue
        #    #code_file.add_element()
        elements = re.findall("import\s+(.+)",line)
        if elements != []:
            print(elements)
            print("MATCH SUCCEED(i)")
            for element in elements:
                code_file.add_element(analyzer.parse_import(-1,arg_import=element[1]))
            continue
    print("SUCCEED")
