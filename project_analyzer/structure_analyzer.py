from code_analyzer import CodeAnalyzer
from file_analyzer import FileAnalyzer
from contrib.structs.file import File
import re


class StructureAnalyzer:
    # 文件分析
    # 提取文件夹下的requirements.txt和*.py文件
    # 调用不同的分析程序
    @staticmethod
    def files_analyze(root_dir=''):
        file_system = FileAnalyzer.file_analyze(root_dir=root_dir)
        if file_system:
            has_tree, file_system_suffix = FileAnalyzer.file_suffix_analyze(
                ['txt', 'py'], file_system)
            print('lib tree:')
            file_system_suffix.print_tree()
            return file_system_suffix
        return None

    # 结构分析
    # 通过调用分析文件分析结果中的import语句，整合出所有外部调用结构
    @staticmethod
    def structure_analyze(root_file=None):
        if not root_file:
            return None
        if not isinstance(root_file, File):
            return None
        if root_file.file_type == "folder":
            has_file = False
            file_list = []
            for file in root_file.owns:
                analyzed_file = StructureAnalyzer.structure_analyze(file)
                if analyzed_file:
                    has_file = True
                    file_list.append(analyzed_file)
            if not has_file:
                return None
            else:
                root_node = File(filename=root_file.filename,
                                 file_type="folder",
                                 owned_by=None)
                root_node.add(file_list)
                return root_node
        elif root_file.get_suffix == "py":
            return CodeAnalyzer.code_analyze(root_file, "python")
        elif re.match(r".*requirement.*\.txt", root_file.filename):
            return CodeAnalyzer.code_analyze(root_file, "python_requirements")
        else:
            return None

    @staticmethod
    def get_output_list(result_tree, current_file=None):
        output_result = []
        if not result_tree:
            return []
        if not current_file:
            current_file = result_tree
        if current_file.owns:
            for file in current_file.owns:
                output_result += StructureAnalyzer.get_output_list(result_tree, file)
            return output_result
        for import_element in current_file.code_elements:
            if StructureAnalyzer.check_import_exists(current_file, import_element):
                output_result.append(import_element)
        return output_result

    @staticmethod
    def check_import_exists(current_file, current_import):
        return True


if __name__ == "__main__":
    ana_tree = StructureAnalyzer.files_analyze(
        'E:\\Works\\python-import-analyzer')
    struct_result = StructureAnalyzer.structure_analyze(ana_tree)
    output_result = StructureAnalyzer.get_output_list(struct_result)
    print('succeed')
