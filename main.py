import os
import json
import contextlib
from typing import List, Optional
from urllib.parse import urlencode

import dotenv
import requests
from pydantic import BaseModel

dotenv.load_dotenv()

APIKEY = os.getenv("APIKEY")

class Movie(BaseModel):
	m_id: str
	title: str
	rating: float
	release_year: int
	genere: List[str]

'''
successful e.g.
http://www.omdbapi.com/?t=Kong%3A+Skull+Island
http://www.omdbapi.com/?t=Dhoom+2
http://www.omdbapi.com/?t=Dum

failure e.g.
https://www.omdbapi.com/?t=John+Wick%3A+Chapter+Two&apikey=9fd2eb91
{"Response":"False","Error":"Movie not found!"}
'''

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

def fetch_from_inet(url: str) -> Optional[Movie]:
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
	breakpoint()
	return ans

def load_database() -> List[Movie]:
	with open("localdatabase.json", mode='rt') as fo:
		raw = json.load(fo)
	all_movies = [
		Movie(**element)
		for element in raw["movies"]
	]
	return all_movies

def save_database(all_movies: List[Movie]) -> bool:
	# https://pydantic-docs.helpmanual.io/usage/exporting_models/#modeljson
	try:
		with open("localdatabase.json", mode='wt') as fo:
			fo.write(
				'{"movies": [%s]}' % \
				",".join(el.json() for el in all_movies)
			)
	except:
		return False
	else:
		return True

def find_all_movies(by, target, all_movies) -> List[Movie]:
	if by not in ["rating", "release_year", "genere"]:
		return None
	matches = list()
	cmp = {
		"genere": lambda m, t: t in m,
		"rating": lambda m, t: m >= float(t),
		"release_year": lambda m, t: m == int(t)
	}[by]
	for movie in all_movies:
		value = getattr(movie, by)
		if cmp(value, target):
			matches.append(movie)
	return matches

def find_movie(by: str, target: str, all_movies: List[Movie]) -> Optional[Movie]:
	if by not in ["m_id", "title"]:
		return None
	for movie in all_movies:
		value = getattr(movie, by)
		if target == value:
			return movie
	else:
		if by == "title":
			possible = fetch_from_inet(
				build_req_url(target)
			)
			if possible:
				all_movies.append(possible)
				print(save_database(all_movies))
				return possible
			else:
				return None
		else:
			return None

if __name__ == "__main__":
	import sys
	print(find_all_movies(sys.argv[1], sys.argv[2], load_database()))
