from decouple import config

# TODO; move tatum base url to settings file.
TATUM_BASE_URL = config("TATUM_BASE_URL")
TATUM_API_KEY = config("TATUM_API_KEY")
