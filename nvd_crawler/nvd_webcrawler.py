import requests
import json
import os


class NVDWebCrawler:
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
                    "https://services.nvd.nist.gov/rest/json/cves/1.0",
                    {"keyword" : package_name})
                response = res.json()
                # print(json.dumps(response,sort_keys=True, indent=2))

                path = './output/%s/' % package_name
                if not os.path.exists(path):
                    # make dirs for packages that have not been parsed
                    os.makedirs(path)
                f = open(path + 'cve.json', 'w+')
                json.dump(response, f, indent=2)
                f.close()
                print('[parse succeed]package_name: %s' % package_name)
            except Exception as e:
                print('[exception]Exception occurred: %s' % e.__str__())
                print('[parse failed]package_name: %s' % package_name)
                self.result[package_name] = {"Exception": e.__str__()}
                continue
        return self.result

if __name__ == "__main__":
    package_names = ["pip", "requests", "django"]
    wrapper = NVDWebCrawler(package_names)
    print(wrapper.parse())
