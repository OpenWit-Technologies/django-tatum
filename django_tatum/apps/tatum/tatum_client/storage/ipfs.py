from tatum_client import creds
from utils.requestHandler import RequestHandler
import utils.utility as utils


class IPFSStorage:
    
    def store_data(self, file: str):
        requestUrl = f"{creds.TATUM_BASE_URL}ipfs"
        Handler = RequestHandler(requestUrl, {"Content-Type": "multipart/form-data", "x-api-key": creds.TATUM_API_KEY})
        payload = {
            "data": file
        }
        response = Handler.post(data=payload)
        return response.json()
    
    def get_data(self, id: str):
        requestUrl = f"{creds.TATUM_BASE_URL}ipfs/{id}"
        Handler = RequestHandler(requestUrl, {"x-api-key": creds.TATUM_API_KEY})
        response = Handler.get()
        return response.json()