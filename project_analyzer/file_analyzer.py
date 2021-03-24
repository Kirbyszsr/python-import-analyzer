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
        if not isinstance(suffix,(str,list)):
            return False, root_file
        suffix = [suffix.lower()] if isinstance(suffix,str) else [sub.lower() for sub in suffix]
        root = root_file
        root_has_suffix_file = False
        if root_file is None or not isinstance(root, File):
            return False, None
        else:
            if root_file.is_type("file"):
                # 检查要使用大小写不敏感的搜索方式
                is_suffix_file = root_file.get_suffix in suffix
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
                    # 这里无论文件夹下是否存在对应后缀文件，都需要返回一个根目录文件的拷贝
                    # 以防止根目录下不存在对应后缀文件时，返回None空文件导致错误
                    return root_has_suffix_file, file_node if root_has_suffix_file else root_file.__copy__()


if __name__ == "__main__":
    file_system = FileAnalyzer.file_analyze(root_dir='E:\\新建文件夹')
    file_system.print_tree()
    if file_system:
        has_tree,file_system_suffix_Lib = FileAnalyzer.file_suffix_analyze('jpg', file_system)
        print('lib tree:')
        file_system_suffix_Lib.print_tree()
        print('file_result:')
        find_results = file_system_suffix_Lib.find('img_5425.jpg')
        find_results.print_tree()
        print('concrete_url:',find_results.get_concrete_url(base_url=''))

