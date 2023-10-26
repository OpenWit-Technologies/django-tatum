import requests


class RequestHandler:
    def __init__(self, url, headers):
        self.url = url
        self.headers = headers

    def get(self, *args, **kwargs):
        return requests.get(self.url, headers=self.headers, *args, **kwargs)

    def post(self, data = None, *args, **kwargs):
        return requests.post(self.url, headers=self.headers, json=data, *args, **kwargs)

    def put(self, data, *args, **kwargs):
        return requests.put(self.url, headers=self.headers, json=data, *args, **kwargs)

    def delete(self, *args, **kwargs):
        return requests.delete(self.url, headers=self.headers, *args, **kwargs)

    def patch(self, data, *args, **kwargs):
        return requests.patch(self.url, headers=self.headers, json=data, *args, **kwargs)
