from pypi_crawler.pypi_webcrawler import PyPIWebCrawler
from pypi_crawler.pypi_analyzer import PyPIAnalyzer
from contrib.elements.package import Package


class PyPIDependencyAnalyzer:
    def __init__(self, dependency_list=None):
        if dependency_list is None:
            dependency_list = []
        self.dependency_list = dependency_list
        self.dependency_packages = []
        self.error_list = []

    def analyze(self):
        remained_dependency_list = self.dependency_list.copy()
        parsed_package_names = []
        parsed_packages = []
        while remained_dependency_list:
            print("[PyPIDependencyAnalyzer]Remained_dependency_list:", remained_dependency_list)
            package_info = PyPIDependencyAnalyzer.get_dependencies(remained_dependency_list)
            for (package_name, info) in package_info.items():
                print("[PyPIDependencyAnalyzer]Analyzing:%s" % package_name)
                pack_analyzer = PyPIAnalyzer(info)
                print("[pypi_analyzer]Available versions:")
                versions = pack_analyzer.available_versions([])
                print(versions)
                if not versions:
                    self.error_list.append(AssertionError('Package %s does not have an available version'
                                                          % package_name))
                print("[pypi_analyzer]parse_requirement_dist:")
                current_package_imports = pack_analyzer.parse_requirement_dist()
                print(current_package_imports)

                current_package = Package(package_name)
                current_package_include_names = [package.name
                                                 for package
                                                 in pack_analyzer.requirement_list]
                current_package.tree_include_packages = pack_analyzer.requirement_list
                current_package.include_package_names = current_package_include_names
                parsed_package_names.append(package_name)
                parsed_packages.append(current_package)
                if package_name in self.dependency_list:
                    self.dependency_packages.append(current_package)

                remained_dependency_list.remove(package_name)
                for pack_name in current_package_include_names:
                    if pack_name not in parsed_package_names \
                            and pack_name not in remained_dependency_list:
                        remained_dependency_list.append(pack_name)
                for pack in parsed_packages:
                    if package_name in pack.include_package_names:
                        pack.include_packages.append(current_package)

        return self.dependency_packages, parsed_package_names

    def check_dependencies(self):
        error_list = []
        dependency_list = self.dependency_list
        return error_list, dependency_list

    # package_names : 纯包名的list(不带限制)
    @staticmethod
    def get_dependencies(package_names=None):
        if package_names is None:
            package_names = []
        if isinstance(package_names, str):
            package_names = [package_names]
        assert (isinstance(package_names, list))
        dependency_crawlers = PyPIWebCrawler(package_names)
        return dependency_crawlers.parse()


if __name__ == "__main__":
    sample_package_names = ['124214214']
    # sample_package_names = ['requests']
    # package_names = ['django', 'pip', 'requests']
    analyzer = PyPIDependencyAnalyzer(sample_package_names)
    result_package, result_names = analyzer.analyze()
    print("[PyPIDependencyAnalyzer]OK")
    print("[PyPIDependencyAnalyzer]parsed_package_names:")
    print(result_names)
