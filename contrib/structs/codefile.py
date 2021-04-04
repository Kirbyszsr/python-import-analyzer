# Codefile.py
# 用于定义项目中所分析的源代码文件

from contrib.structs.file import File
from contrib.elements.codeblock import CodeElement, Class, Method, Variate, Import


class CodeFile(File):
    """
     定义项目中所所分析的源代码文件
     """

    def __init__(self, filename, owned_by=None):
        super(
            CodeFile,
            self).__init__(
            filename=filename,
            file_type="file",
            owned_by=owned_by)
        # 储存标识出的code block记号
        self.code_elements = []
        self.code_type = 'unknown'

    # 查看文件中所有Class对象
    def classes(self):
        classes = []
        for element in self.code_elements:
            if isinstance(element, Class):
                classes += element
        return classes

    # 查看文件中所有Method对象
    def methods(self):
        methods = []
        for element in self.code_elements:
            if isinstance(element, Method):
                methods += element
        return methods

    # 查看文件中所有Variable对象
    def variables(self):
        variables = []
        for element in self.code_elements:
            if isinstance(element, Variate):
                variables += element
        return variables

    # 查看文件中所有Import对象
    def imports(self):
        imports = []
        for element in self.code_elements:
            if isinstance(element, Import):
                imports += element
        return imports

    # 为文件添加一个或多个代码识别元素
    def add_element(self, element):
        # 添加单个元素
        if isinstance(element, CodeElement):
            self.code_elements.append(element)
            return True
        # 添加多个元素
        elif isinstance(element, list):
            list_succeed = True
            for ele in element:
                is_succeed = self.add_element(ele)
                if not is_succeed:
                    list_succeed = False
            return list_succeed
        else:
            return False

    # 为文件删去一个或多个代码识别元素
    def remove_element(self, element):
        # 删去单个元素
        if isinstance(element, CodeElement):
            self.code_elements.remove(element)
        # 删去多个元素
        elif isinstance(element, list):
            for ele in element:
                self.code_elements.remove(ele)
        return


if __name__ == "__main__":
    pass
