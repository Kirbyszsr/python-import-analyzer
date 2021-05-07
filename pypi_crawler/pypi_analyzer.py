from contrib.elements.codeblock import Import
from contrib.elements.versions import Version
import json
import re


class PyPIAnalyzer:
    def __init__(self, basic_info: dict):
        self.basic_info = basic_info
        self.requirement_list = []

    def available_versions(self, version_str_list=None):
        if version_str_list is None:
            version_str_list = []
        if not version_str_list:
            return self.basic_info["released_versions"] \
                if "released_versions" in self.basic_info.keys() else []
        available_versions = [Version(version) for version in self.basic_info["released_versions"]]
        checked_versions = []
        symbols = ['<', '<=', '>', '>=', '==', '!=']
        versions = [[], [], [], [], [], []]
        version_dict = dict(zip(symbols, versions))
        for version_str in version_str_list:
            elements = re.findall("([!><=]+)([0-9].*)", string=version_str)[0]
            for symbol in symbols:
                if elements[0] == symbol:
                    version_dict[symbol].append(Version(elements[1]))
        for version in available_versions:
            is_available = True
            for lt_version in version_dict['<']:
                if not version < lt_version:
                    is_available = False
            for le_version in version_dict['<=']:
                if not version <= le_version:
                    is_available = False
            for mt_version in version_dict['>']:
                if not version > mt_version:
                    is_available = False
            for me_version in version_dict['>=']:
                if not version >= me_version:
                    is_available = False
            for eq_version in version_dict['==']:
                if not version == eq_version:
                    is_available = False
            for ne_version in version_dict['!=']:
                if not version != ne_version:
                    is_available = False
            if is_available:
                checked_versions.append(version)
        return [version.version_str for version in checked_versions]

    def parse_requirement_dist(self):
        requirements_list = self.basic_info["requires_dist"] \
            if "requires_dist" in self.basic_info.keys() else []
        if not requirements_list:
            return []
        parsed_requirements_list = []
        for requirement in requirements_list:
            requirement_index = requirement.find(';')
            if requirement_index != -1:
                parsed_requirements_list.append(requirement[:requirement_index].strip())
            else:
                parsed_requirements_list.append(requirement.strip())
        parsed_requirements_imports = []
        for parsed_requirement in parsed_requirements_list:
            elements = re.findall(
                "(.+) \((.+)\)", parsed_requirement)
            if elements:
                for element in elements:
                    parsed_requirements_imports.append(
                        Import(name=element[0].strip(),
                               filename=self.basic_info["name"],
                               line=-1,
                               from_element=element[0].strip(),
                               import_element="*",
                               as_element=element[0].strip(),
                               version=element[1].strip()
                               )
                    )
            else:
                parsed_requirements_imports.append(
                    Import(name=parsed_requirement.strip(),
                           filename=self.basic_info["name"],
                           line=-1,
                           from_element=parsed_requirement.strip(),
                           import_element="*",
                           as_element=parsed_requirement.strip(),
                           version='*'
                           )
                )
        self.requirement_list = parsed_requirements_imports
        return parsed_requirements_list


if __name__ == "__main__":
    package_names = ['django', 'pip', 'requests']
    for package_name in package_names:
        path = './output/%s/' % package_name
        requirement_simple_filename = path + 'requirement-simple.json'
        with open(requirement_simple_filename) as f:
            print("[pypi_analyzer]Open file: %s" % requirement_simple_filename)
            result = json.load(f)
            # print(result)
        analyzer = PyPIAnalyzer(result)
        print("[pypi_analyzer]Available versions:")
        print(analyzer.available_versions([]))
        print("[pypi_analyzer]parse_requirement_dist:")
        print(analyzer.parse_requirement_dist())
