import requests
import json
import os


class PyPIWebCrawler:
    def __init__(self,packages):
        """
        PYPI WebCrawler
        :param packages: list[str]
        a list of name of packages
        """
        assert(isinstance(packages,list))
        for element in packages:
            assert(isinstance(element,str))
        self.packages = packages

    def parse(self):
        for package_name in self.packages:
            try:
                res = requests.get("https://pypi.org/pypi/%s/json" % package_name)
                response = res.json()
                # print(json.dumps(response,sort_keys=True, indent=2))
                path = './output/%s/' % package_name
                if not os.path.exists(path):
                    # make dirs for packages that have not been parsed
                    os.makedirs(path)
                f = open(path + 'requirement.json','a+')
                json.dump(response,f)
                f.close()
                print('[parse succeed]package_name: %s' % package_name)
            except Exception as e:
                print('[exception]Exception occured: %s' % e.__str__())
                print('[parse failed]package_name: %s' % package_name)
                continue


if __name__ == "__main__":
    package_names = ["pip","requests","django"]
    wrapper = PyPIWebCrawler(package_names)
    wrapper.parse()