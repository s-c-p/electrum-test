from ds import Movie
from inet import fetch
from db import save_database
from typing import List, Optional

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
			possible = fetch(target)
			if possible:
				all_movies.append(possible)
				print(save_database(all_movies))
				return possible
			else:
				return None
		else:
			return None

