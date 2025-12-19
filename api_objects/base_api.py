# api_objects/base_api.py
from playwright.sync_api import APIRequestContext

class BaseApi:
    def __init__(self, context: APIRequestContext):
        self.context = context  # 把 Playwright 的 request 工具存起来

    def get(self, url, **kwargs):
        return self.context.get(url, **kwargs)

    def post(self, url, **kwargs):
        return self.context.post(url, **kwargs)

    def put(self, url, **kwargs):
        return self.context.put(url, **kwargs)

    def delete(self, url, **kwargs):
        return self.context.delete(url, **kwargs)