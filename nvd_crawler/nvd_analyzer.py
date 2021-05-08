from nvd_crawler.nvd_webcrawler import NVDWebCrawler


class NVDAnalyzer:
    def __init__(self, dependency_list=None):
        if dependency_list is None:
            dependency_list = []
        self.dependency_list = dependency_list
        self.cve_result = {}

    def analyze(self):
        wrapper = NVDWebCrawler(self.dependency_list)
        self.cve_result = wrapper.parse()


if __name__ == "__main__":
    package_names = ["hnya123", "pip", "requests", "django"]
    analyzer = NVDAnalyzer(package_names)
    analyzer.analyze()
    print(analyzer.cve_result)