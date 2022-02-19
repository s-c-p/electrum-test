import json
from typing import List, Optional

from fastapi import FastAPI, Request

from db import Movie, find_all_movies, find_movie, create_db_tables_and_testdata

app = FastAPI()
create_db_tables_and_testdata()

@app.get("/searchOne/t/{title}")
def get_movie_by_id(title: str):
	return find_movie("title", title)

@app.get("/searchOne/id/{movie_id}")
def get_movie_by_id(movie_id: str):
	return find_movie("m_id", movie_id)

@app.get("/searchAll/rating/{r}")
def get_movies_by_rating(r: float):
	return find_all_movies("rating", r)

@app.get("/searchAll/genere/{g}")
def get_movies_by_genere(g: str):
	return find_all_movies("genere", g)

@app.get("/searchAll/year/{y}")
def get_movies_by_year(y: int):
	return find_all_movies("release_year", y)
