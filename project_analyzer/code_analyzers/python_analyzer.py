from contrib.structs.file import File
from contrib.structs.codefile import CodeFile
from contrib.elements.codeblock import Class, Method, Variate, Import
from project_analyzer.code_analyzers.analyzer import Analyzer
import re
import ast
import astunparse


class PythonAnalyzer(Analyzer):

    def __init__(self, code_file):
        super(PythonAnalyzer, self).__init__(code_file)
        # self.row = 0
        # 当前阅读的行数数据
        # self.rows = []
        self.current_line = 0
        self.lines = None

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
                       line=line,
                       owns=None)

    def parse_import(
            self,
            line,
            arg_import,
            arg_as=None,
            arg_from=None,
            arg_version='*'):
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
        if not isinstance(self.code_file, File):
            raise TypeError(
                '代码的分析对象必须是一个contrib.structs.File对象,而对象的类型是' + str(type(self.code_file)))
        if self.code_file.file_type is not "file":
            raise TypeError('代码的分析对象必须是一个文件,而对象是一个' + self.code_file.file_type)

        # 创建一个CodeFile对象以返回
        code_file = CodeFile(filename=self.code_file.filename,
                             owned_by=None)
        code_file.code_type = 'python'

        code_lines = self.read_file()
        self.rows = code_lines
        self.parse_lines()

        file_url = self.code_file.get_concrete_url()

        code_file = CodeFile(file_url)
        analyzer = PythonAnalyzer(code_file)

        # 行记录
        import_line = []
        def_line = []
        class_line = []
        equal_line = []

        for line in self.rows:
            # 去除单行注释
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
        # print(import_line)
        # print(def_line)
        # print(class_line)
        # print(equal_line)

        # 要使用;对同一行语句进行切块

        for line in import_line:
            elements = re.findall(
                "from\\s+(.+)\\s+import\\s+(.+)\\s+as\\s+(.+)", line)
            if elements:
                # print(elements)
                # print("MATCH SUCCEED(fia)")
                for element in elements:
                    code_file.add_element(
                        analyzer.parse_import(-1,
                                              arg_from=element[0].strip(),
                                              arg_import=element[1].strip(),
                                              arg_as=element[2].strip()))
                continue

            elements = re.findall("from\\s+(.+)\\s+import\\s+(.+)", line)
            if elements:
                # print(elements)
                # print("MATCH SUCCEED(fi)")
                for element in elements:
                    for arg_import in element[1].strip().split(','):
                        code_file.add_element(analyzer.parse_import(-1,
                                                                    arg_from=element[0].strip(),
                                                                    arg_import=arg_import.strip()))
                continue

            elements = re.findall("import\\s+(.+)as\\s+(.+?)", line)
            if elements:
                # print(elements)
                # print("MATCH SUCCEED(ia)")
                for element in elements:
                    code_file.add_element(analyzer.parse_import(-1,
                                                                arg_from=element[0].strip(),
                                                                arg_import=element[1].strip()))
                continue
            #    #code_file.add_element()
            elements = re.findall("import\\s+(.+)", line)
            if elements:
                # print(elements)
                # print("MATCH SUCCEED(i)")
                for element in elements:
                    import_elements = element.strip().split(',')
                    import_elements = [import_elements] \
                        if isinstance(import_elements, str) \
                        else import_elements
                    for arg_import in import_elements:
                        code_file.add_element(
                            analyzer.parse_import(-1, arg_import=arg_import.strip()))
                continue

        self.rows = code_lines
        code_file.code_type = 'python'
        return code_file

    def read_file(self):
        """
        读取文件的内容
        :return: 一个list, 包含该文件的所有row
        """
        # 获取url
        code_file_url = self.code_file.get_concrete_url(base_url='')
        f = None
        encoding_types = ['utf-8', 'iso-8859-1']
        while True:
            f_lines = None
            for encoding_type in encoding_types:
                try:
                    f = open(code_file_url, encoding=encoding_type, mode='r')
                    f_lines = f.readlines()
                    break
                except UnicodeDecodeError:
                    # for UnicodeDecodeError for utf-8
                    continue
                finally:
                    if f:
                        f.close()
            return f_lines if f_lines else []

    def read_line(self, row=None):
        """
        :param self:
        :param row:
        :return: 一行处理过后的代码数据; 读取本行所占用的行数
        当前行指针向下移动若干行,行数等于在处理过程中阅读的行数

        * 如果有注释数据，则略过这些注释数据
        """
        return None

    def parse_lines(self):
        """
        :return:

        先行对line中可能出现的单行注释或者多行注释
        进行去注释操作
        """

        print(self.code_file.filename)
        try:
            a = ast.parse(''.join(row for row in self.rows))
            b = astunparse.unparse(a)
            self.rows = b.split("\n")
            print('[parse_lines]parse %s succeed' % self.code_file.fullname)
        except:
            print('[parse_lines]parse %s error, using normal mode' % self.code_file.filename)

        row_count = 0
        in_multiple_note = False
        multiple_note_flag = None
        multiple_note_row = -1
        for raw_line in self.rows:
            clear_line = raw_line
            if in_multiple_note and clear_line.find(multiple_note_flag) == -1:
                self.rows[row_count] = '\n'
                row_count += 1
                continue
                # 忽略内容
            elif in_multiple_note:
                in_multiple_note = False
                clear_line = clear_line[raw_line.find(
                    multiple_note_flag) + len(multiple_note_flag):]
                multiple_note_flag = None

            # 去除单行中可能出现的多行注释
            # 如果仍存在多行注释记号,记录这个多行注释符号的位置，并删除多行注释符号后存在的内容
            # 要先行去除多行注释符号 """ '''或者 #在'' ""内的情况

            clear_line = re.sub(r'([^"])"[^"]+"([^"]|$)', r"\1\2", clear_line)
            clear_line = re.sub(r'([^\'])\'[^\']+\'([^\']|$)', r"\1\2", clear_line)
            # todo: * +都试试
            # 删除单行注释
            clear_line = re.sub(r'#.*$', "", clear_line)

            while True:
                single_quotes = clear_line.find("\'\'\'")  # '''
                multiple_quotes = clear_line.find("\"\"\"")  # """
                if single_quotes == -1 and multiple_quotes == -1:
                    break
                elif single_quotes == -1:
                    if not clear_line == re.sub(r'""".*"""', "", clear_line):
                        clear_line = re.sub(r'""".*"""', "", clear_line)
                        continue
                    in_multiple_note, multiple_note_flag = True, '"""'
                    multiple_note_row = row_count
                    clear_line = re.sub(r'""".*$', "", clear_line)
                    break
                elif multiple_quotes == -1:
                    if not clear_line == re.sub(r"'''.*'''", "", clear_line):
                        clear_line = re.sub(r"'''.*'''", "", clear_line)
                        continue
                    in_multiple_note, multiple_note_flag = True, "'''"
                    multiple_note_row = row_count
                    clear_line = re.sub(r"'''.*$", "", clear_line)
                    break

            # 删除掉可能出现的引用'' ""内的内容
            clear_line = re.sub(r"\'.*\'([^'])", r"''\1", clear_line)
            clear_line = re.sub(r'\".*\"([^"])', r'""\1', clear_line)

            self.rows[row_count] = clear_line
            row_count += 1
        if in_multiple_note:
            raise AssertionError(
                "fileName" +
                self.code_file.filename +
                '在第' +
                str(multiple_note_row) +
                '行中找到了未匹配的多行注释符号' +
                multiple_note_flag)
        return True

    def next_line(self):
        return None


if __name__ == "__main__":
    # PythonAnalyzer.read_file()
    file_url = "E:\\Works\\python-import-analyzer\\project_analyzer\\code_analyzers\\python_analyzer.py"
    # try:
    #    file = open(file_url,encoding='utf-8',mode='r')
    #    lines = file.readlines()
    # finally:
    #    if file:
    #        file.close()
    #    if not lines:
    #        lines = []
    sample_code_file = File(file_url)
    analyzer = PythonAnalyzer(sample_code_file)
    require_file = analyzer.analyze()
    print('ok')
