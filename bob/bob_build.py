class BobBuild:
    STATUS_SUCCESS = "success"
    STATUS_FAILURE = "failed"


    def __init__(self, name=None, result=None, download_urls=None, original_build=None):
        self.name = name
        self.result = result
        if download_urls == None:
            self.download_urls = []
        else:
            self.download_urls = download_urls
        self.original_build = original_build

    def is_build_successful(self):
        return self.result == BobBuild.STATUS_SUCCESS
