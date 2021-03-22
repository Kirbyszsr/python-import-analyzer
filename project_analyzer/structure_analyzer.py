from code_analyzer import CodeAnalyzer
from file_analyzer import FileAnalyzer


class StructureAnalyzer:
    # 文件分析
    # 提取文件夹下的requirements.txt和*.py文件
    # 调用不同的分析程序
    @staticmethod
    def files_analyze(root_dir=''):
        analyzer = CodeAnalyzer()
        return analyzer.analyze()

    # 结构分析
    # 通过调用分析文件分析结果中的import语句，整合出所有外部调用结构
    @staticmethod
    def structure_analyze(root_file=None):
        pass


if __name__ == "__main__":
    a = ['jpg','GIF']
    b = [string.lower() for string in a]
    print(a)
    print(b)