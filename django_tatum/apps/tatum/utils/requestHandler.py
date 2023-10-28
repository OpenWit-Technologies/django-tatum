import requests


class RequestHandler:
    def __init__(self, url, headers):
        self.url = url
        self.headers = headers

    def get(self, *args, **kwargs):
        return requests.get(
            self.url,
            headers=self.headers,
            *args,
            **kwargs,
        )

    def post(self, data, *args, **kwargs):
        return requests.post(
            self.url,
            headers=self.headers,
            json=data,
            *args,
            **kwargs,
        )

    def put(self, data, *args, **kwargs):
        return requests.put(
            self.url,
            headers=self.headers,
            json=data,
            *args,
            **kwargs,
        )

    def delete(self, *args, **kwargs):
        return requests.delete(
            self.url,
            headers=self.headers,
            *args,
            **kwargs,
        )

    def patch(self, data, *args, **kwargs):
        return requests.patch(
            self.url,
            headers=self.headers,
            json=data,
            *args,
            **kwargs,
        )

    # TODO: Set up the following private handlers:
    # 1. _200_response_handler: to handle 200 response status codes
    # 2. _400_response_handler: to handle 400 response status codes
    # 3. _401_response_handler: to handle 401 response status codes
    # 4. _404_response_handler: to handle 404 response status codes
    # 5. _500_response_handler: to handle 500 response status codes
