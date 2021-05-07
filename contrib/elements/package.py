class Package:
    def __init__(self, package_name, include_packages=[], project_tree=None):
        assert(isinstance(include_packages,list))
        self.package_name = package_name
        self.include_packages = include_packages
        self.include_package_names = []
        self.tree_include_packages = []
        self.project_tree = project_tree
        self.error_list = []

    def get_include_packages(self):
        return self.include_packages + self.tree_include_packages

    def get_include_packages_str_list(self):
        return [package.package_name for package in self.get_include_packages()]

    def add_include_packages(self, package):
        if isinstance(package,Package):
            self.include_packages.append(package)
            return package
        elif isinstance(package,str):
            pak = Package(package_name=package)
            self.include_packages.append(pak)
            return pak
        elif isinstance(package,list):
            succeed_pack = []
            for pak in package:
                pack = self.add_include_packages(pak)
                if pack:
                    succeed_pack.append(pack)
            return succeed_pack
        else:
            return None

    def __eq__(self, other):
        assert(isinstance(other,Package))
        return self.package_name == other.package_name
