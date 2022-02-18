import os
import dotenv
import requests
from ds import Movie
from typing import Optional
from urllib.parse import urlencode

dotenv.load_dotenv()
APIKEY = os.getenv("APIKEY")

def build_req_url(title: str) -> str:
	''' create valid url for given title, supply apikey
	#tested-working
	'''
	BASE_URL = f"https://www.omdbapi.com/?"
	payload = {
		"t": title,
		"apikey": APIKEY
	}
	suffix = urlencode(payload, safe='')
	url = BASE_URL + suffix
	return url

def fetch(title: str) -> Optional[Movie]:
	url = build_req_url(title)
	res = requests.get(url)
	d = res.json()
	if d["Response"] == "True":
		dct = {
			"m_id": d["imdbID"],
			"title": d["Title"],
			"rating": float(d["imdbRating"]),
			"release_year": int(d["Released"].split(" ")[-1]),
			"genere": d["Genre"].split(", ")
		}
		ans = Movie.parse_obj(dct)
	else:
		ans = None
	return ans

