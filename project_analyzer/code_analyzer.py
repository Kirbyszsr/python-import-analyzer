from project_analyzer.code_analyzers.python_analyzer import PythonAnalyzer
from project_analyzer.code_analyzers.requirement_analyzer import RequirementAnalyzer

__all__ = "CodeAnalyzer"


class CodeAnalyzer:

    # 代码分析器
    # 输入:
    # code_file 一个经过file_analyzer处理过的File对象，它的类型是文件
    # type 文件的代码类型，依据代码类型确定分析代码所使用的
    # 暂时预定支持的文件范围: python文件, python requirement文件, (后期版本会尝试加入java文件支持)

    # 输出：一个CodeFile或RequirementFile对象(或JavaCodeFile对象)，
    #       具体对象类型依据识别出的代码类型决定
    # 基于原有File对象，同时包含Code的文件信息
    @staticmethod
    def code_analyze(code_file,code_type='python'):
        if code_type == 'python':
            return CodeAnalyzer.python_analyze(code_file)
        elif code_type == 'python_requirements' :
            return CodeAnalyzer.python_requirements_analyze(code_file)
        elif code_type == 'java':
            return CodeAnalyzer.java_analyze(code_file)
        else:
            return NotImplemented

    @staticmethod
    def python_analyze(code_file):
        return PythonAnalyzer(code_file).analyze()

    @staticmethod
    def python_requirements_analyze(code_file):
        return RequirementAnalyzer(code_file).analyze()

    @staticmethod
    def java_analyze(code_file):
        return NotImplemented
