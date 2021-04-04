from contrib.structs.file import File
from contrib.elements.codeblock import Import


class RequirementFile(File):
    """
     定义项目中所所分析的外部依赖定义文件
     """
    def __init__(self,filename,owned_by=None):
        super(RequirementFile,self).__init__(filename=filename, file_type="file", owned_by=owned_by)
        # 储存标识出的codeblock记号
        self.code_elements = []

    # 查看文件中所有Import对象
    def imports(self):
        return self.code_elements

    # 为文件添加一个或多个代码识别元素
    def add_element(self,element):
        # 添加单个元素
        if isinstance(element,Import):
            self.code_elements.append(element)
            return True
        # 添加多个元素
        elif isinstance(element,list):
            list_succeed = True
            for ele in element:
                is_succeed = self.add_element(ele)
                if not is_succeed:
                    list_succeed = False
            return list_succeed
        else:
            return False

    def remove_element(self,element):
        # 删去单个元素
        if isinstance(element,Import):
            self.code_elements.remove(element)
        # 删去多个元素
        elif isinstance(element,list):
            for ele in element:
                self.code_elements.remove(ele)
        return