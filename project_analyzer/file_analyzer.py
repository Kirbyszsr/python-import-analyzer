import os
from contrib.structs.file import File


# 文件分析方法
class FileAnalyzer:

    # 文件结构分析器
    @staticmethod
    def file_analyze(root_dir='',root_file=None):
        root = root_file if root_file is not None else File(root_dir,'folder')
        for file in os.listdir(root_dir):
            if os.path.isdir(root_dir + '\\' + file):
                new_folder = File(file.title(), 'folder')
                root.add(new_folder)
                url = new_folder.get_concrete_url()
                FileAnalyzer.file_analyze(url,new_folder)
            else:
                new_file = File(file.title(), 'file')
                root.add(new_file)

        return root

    # 文件后缀分析
    # 为文件寻找到一棵最小文件树，使得里面的文件全部包含同一个子域名
    @staticmethod
    def file_suffix_analyze(suffix=None,root_file=None):
        root = root_file
        root_has_suffix_file = False
        if root_file is None or not isinstance(root,File):
            return False,None
        else:
            if root_file.is_type("file"):
                is_suffix_file = root_file.get_suffix == suffix
                if is_suffix_file:
                    file_node = root_file.__copy__()
                    return True, file_node
                else:
                    return False, None
            else:
                if root_file.is_type("folder"):
                    file_node = root_file.__copy__()
                    for file in root_file.owns:
                        has_suffix_file, child_file_node = FileAnalyzer.file_suffix_analyze(suffix,file)
                        if has_suffix_file:
                            root_has_suffix_file = True
                            file_node.add(child_file_node)
                    return root_has_suffix_file, file_node if root_has_suffix_file else None


if __name__ == "__main__":
    file_system = FileAnalyzer.file_analyze(root_dir='D:\\BaiduNetdiskDownload\\MATLAB\\R2010b\\extern')
    file_system.print_tree()
    has_tree,file_system_suffix_Lib = FileAnalyzer.file_suffix_analyze('Lib',file_system)
    print('lib tree:')
    file_system_suffix_Lib.print_tree()
