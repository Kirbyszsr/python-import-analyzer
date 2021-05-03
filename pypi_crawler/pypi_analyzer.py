from contrib.elements.codeblock import Import
import json


class PyPIAnalyzer:
    def __init__(self, basic_info: dict):
        self.basic_info = basic_info

    def available_versions(self,version_str_list: list = []):
        if not version_str_list:
            return self.basic_info["released_versions"]
        return self.basic_info["released_versions"]

    def parse_requirement_dist(self):
        requirements_list = self.basic_info["requires_dist"]
        return requirements_list


if __name__ == "__main__":
    package_names = ['django']
    for package_name in package_names:
        path = './output/%s/' % package_name
        requirement_simple_filename = path + 'requirement-simple.json'
        with open(requirement_simple_filename) as f:
            print("[pypi_analyzer]Open file: %s" % requirement_simple_filename)
            result = json.load(f)
            print(result)
        analyzer = PyPIAnalyzer(result)
        print("[pypi_analyzer]Available versions:")
        print(analyzer.available_versions([]))
        print("[pypi_analyzer]parse_requirement_dist:")
        print(analyzer.parse_requirement_dist())