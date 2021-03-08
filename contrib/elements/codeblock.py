# Codeblock.py
# 定义静态代码元素


__all__ = ('CodeElement', 'NestableCodeElement',
           'Class', 'Method', 'Variate', 'Import')


# 一般静态代码元素
class CodeElement(object):
    """
    代码元素通用属性
    """
    def __init__(self, name, type, filename, line):

        if not name or not type or not filename or not line:
            none_list = ""
            for paras,paraname in ([name,'name'],[type,'type'],[filename,'filename'],[line,'line']):
                if not paras:
                    none_list += paraname if none_list == "" else "," + paraname
            raise ValueError('Cannot set None for CodeElement():' + none_list)
        # 代码元素名
        self.name = name
        # 代码元素所在种类名
        self.type = type
        # 代码元素所在文件名
        self.filename = filename
        # 代码元素所在文件行数
        self.line = line
        pass


# 可嵌套的静态代码元素
# Class, Method, Import 可以
class NestableCodeElement(CodeElement):
    def __init__(self, name, type, filename, line, owns):
        # 调用初始化
        super(NestableCodeElement, self).__init__(name,type,filename,line)
        self.owns = owns if owns and owns.isinstance(list) else []


class Class(NestableCodeElement):
    """
    函数类对象
    """
    def __init__(self, name, filename, line, owns):
        super(Class, self).__init__(name=name,
                                    type='Class',
                                    filename=filename,
                                    line=line,
                                    owns=owns)

    def __str__(self):
        return "Class:[className=" + self.name + "]"


class Method(NestableCodeElement):
    """
    函数方法类对象
    """
    def __init__(self, name, filename, line, owns):
        super(Method, self).__init__(name=name,
                                     type='Method',
                                     filename=filename,
                                     line=line,
                                     owns=owns)

    def __str__(self):
        return "Method:[methodName=" + self.name + "]"


class Variate(CodeElement):
    """
    变量对象
    """
    def __init__(self, name, filename, line, owns):
        super(Variate, self).__init__(name=name,
                                      type='Variate',
                                      filename=filename,
                                      line=line,
                                      owns=owns)

    def __str__(self):
        return "Variate:[variateName=" + self.name + "]"


class Import(CodeElement):
    """
    外部调用语句对象
    """
    def __init__(self, name, filename, line, from_element, import_element='*',as_element=None, version='*'):
        super(Import,self).__init__(name=name,
                                    type='Import',
                                    filename=filename,
                                    line=line)
        self.from_element = from_element
        self.import_element = import_element
        self.as_element = as_element if as_element else from_element
        # 预留用版本号
        self.version = version

    def __str__(self):
        return "Import:[ImportName=" + self.name + "]"


if __name__ == '__main__':
    a = CodeElement('a','v','c','a')
    print(a)