import json
from typing import List, Optional

from fastapi import FastAPI, Request

from ds import Movie
from db import load_database
from utils import find_movie, find_all_movies

app = FastAPI()

all_movies = load_database()

@app.get("/searchOne/t/{title}")
def get_movie_by_id(title: str):
	return find_movie("title", title, all_movies)

@app.get("/searchOne/id/{movie_id}")
def get_movie_by_id(movie_id: str):
	return find_movie("m_id", movie_id, all_movies)

@app.get("/searchAll/rating/{r}")
def get_movies_by_rating(r: float):
	return find_all_movies("rating", r, all_movies)

@app.get("/searchAll/genere/{g}")
def get_movies_by_genere(g: str):
	return find_all_movies("genere", g, all_movies)

@app.get("/searchAll/year/{y}")
def get_movies_by_year(y: int):
	return find_all_movies("release_year", y, all_movies)
