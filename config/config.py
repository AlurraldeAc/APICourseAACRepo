from dotenv import load_dotenv
import os

load_dotenv()

token_gorest_api = os.getenv("token")

URL_GOREST = "https://gorest.co.in/public/v2"
HEADERS_GOREST = {
    "Authorization": f"Bearer {token_gorest_api}"
}

