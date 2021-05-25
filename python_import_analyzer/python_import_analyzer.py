from project_analyzer.structure_analyzer import StructureAnalyzer
from pypi_crawler.pypi_dependency_analyzer import PyPIDependencyAnalyzer
from nvd_crawler.nvd_analyzer import NVDAnalyzer


class PythonImportAnalyzer:
    def __init__(self, project_index_root: str):
        self.project_index_root = project_index_root
        self.struct_result = None
        self.import_result = None
        self.cleared_import_result = None
        self.cleared_import_result_list = None

        self.result_package = []
        self.result_names = None

        self.error_list = []

    def analyze(self):
        self.project_analyze()
        self.pypi_analyze()
        self.nvd_analyze()

    def project_analyze(self):
        ana_tree = StructureAnalyzer.files_analyze(
            self.project_index_root)
        struct_result = StructureAnalyzer.structure_analyze(ana_tree)
        import_result = StructureAnalyzer.get_output_list(struct_result)
        cleared_import_result,error_list = StructureAnalyzer.check_result_import_list(import_result)
        self.cleared_import_result_list = \
            [import_element.from_element for import_element in cleared_import_result]
        print(error_list)

    def pypi_analyze(self):
        sample_package_names = self.cleared_import_result_list
        # sample_package_names = ['requests']
        # package_names = ['django', 'pip', 'requests']
        pypi_analyzer = PyPIDependencyAnalyzer(sample_package_names)
        self.result_package, self.result_names = pypi_analyzer.analyze()
        print("[PyPIDependencyAnalyzer]OK")
        print("[PyPIDependencyAnalyzer]parsed_package_names:")
        print(self.result_names)

    def nvd_analyze(self):
        package_names = [package.package_name for package in self.result_package]
        nvd_analyzer = NVDAnalyzer(package_names)
        nvd_analyzer.analyze()

    def show_result(self):
        return "Result for %s:" % self.project_index_root


if __name__ == "__main__":
    work_root = 'E:\\Works\\python-import-analyzer'
    analyzer = PythonImportAnalyzer(work_root)
    analyzer.analyze()
    print(analyzer.show_result())
