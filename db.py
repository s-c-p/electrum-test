import json
from ds import Movie
from typing import List

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

