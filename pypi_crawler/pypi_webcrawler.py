import requests
import json
import os


class PyPIWebCrawler:
    def __init__(self, packages, force_updating=False):
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
        self.force_updating = force_updating

    def parse(self):
        for package_name in self.packages:
            try:
                path = './output/%s/' % package_name
                if not self.force_updating:
                    if os.path.exists(path + 'requirement-simple.json'):
                        print("[PyPIWebCrawler]parsing package %s found requirement-simple.json"
                              % package_name)
                        is_succeed = False
                        f = None
                        try:
                            f = open(path + 'requirement-simple.json', 'r')
                            basic_info = json.load(f)
                            self.result[package_name] = basic_info
                            print("[PyPIWebCrawler]parse succeed - package_name: %s" % package_name)
                            is_succeed = True
                        except Exception as e:
                            print("[PyPIWebCrawler]Error when parsing requirement-simple.json:%s"
                                  % e.__str__())
                            print("[PyPIWebCrawler]now downloading data")
                        finally:
                            if f:
                                f.close()
                        if is_succeed:
                            continue
                res = requests.get(
                    "https://pypi.org/pypi/%s/json" %
                    package_name)
                if res.status_code != 200:
                    raise RuntimeError("Internet Error, status code=%d" % res.status_code)
                response = res.json()
                # print(json.dumps(response,sort_keys=True, indent=2))

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
                print('[PyPIWebCrawler]parse succeed - package_name: %s' % package_name)
            except Exception as e:
                print('[PyPIWebCrawler][exception]Exception occurred when parsing %s: %s' % (package_name, e.__str__()))
                print('[PyPIWebCrawler]parse failed - package_name: %s' % package_name)
                self.result[package_name] = {"Exception": e.__str__()}
                continue
        return self.result


if __name__ == "__main__":
    package_names = ["pip", "requests", "django"]
    wrapper = PyPIWebCrawler(package_names)
    print(wrapper.parse())
    print("test")
    print("[PyPI_WebCrawler]OK")
