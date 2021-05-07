import requests
import json
import os


class PyPIWebCrawler:
    def __init__(self, packages):
        """
        PYPI WebCrawler
        :param packages: list[str]
        a list of name of packages
        """
        assert(isinstance(packages, list))
        for element in packages:
            assert(isinstance(element, str))
        self.packages = packages
        self.result = {}

    def parse(self):
        for package_name in self.packages:
            try:
                res = requests.get(
                    "https://pypi.org/pypi/%s/json" %
                    package_name)
                response = res.json()
                # print(json.dumps(response,sort_keys=True, indent=2))

                path = './output/%s/' % package_name
                if not os.path.exists(path):
                    # make dirs for packages that have not been parsed
                    os.makedirs(path)
                f = open(path + 'requirement.json', 'w+')
                json.dump(response, f, indent=2)
                f.close()

                # 提取requirement.json里特定的内容并进行简单保存
                info = response["info"]

                basic_info = {
                    "name": package_name,
                    "description": info["description"],
                    "requires_dist": info["requires_dist"],
                    "requires_python": info["requires_python"],
                    "current_version": info["version"],
                    "released_versions": list(
                        response["releases"].keys())}

                f = open(path + 'requirement-simple.json', 'w+')
                json.dump(basic_info, f, indent=2)
                f.close()

                self.result[package_name] = basic_info
                print('[parse succeed]package_name: %s' % package_name)
            except Exception as e:
                print('[exception]Exception occurred when parsing %s: %s' % (package_name,e.__str__()))
                print('[parse failed]package_name: %s' % package_name)
                self.result[package_name] = {"Exception": e.__str__()}
                continue
        return self.result


if __name__ == "__main__":
    package_names = ["pip", "requests", "django"]
    wrapper = PyPIWebCrawler(package_names)
    print(wrapper.parse())
    print("[PyPI_WebCrawler]OK")
