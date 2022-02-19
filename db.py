import operator
from typing import List, Optional, Any

from ds import Movie
from inet import fetch
from sqlmodel import Field, Relationship, Session, SQLModel, create_engine, select

class SQLMovieGenreLink(SQLModel, table=True):
	movie_id: Optional[str] = Field(
		default=None, foreign_key="sqlmovie.m_id", primary_key=True
	)
	genere_id: Optional[int] = Field(
		default=None, foreign_key="genere.gid", primary_key=True
	)

class Genere(SQLModel, table=True):
	gid: Optional[int] = Field(default=None, primary_key=True)
	tag: str
	movies: List["SQLMovie"] = Relationship(back_populates="generes", link_model=SQLMovieGenreLink)

class SQLMovie(SQLModel, table=True):
	m_id: str = Field(default=None, primary_key=True)
	title: str
	rating: float
	release_year: int
	generes: List[Genere] = Relationship(back_populates="movies", link_model=SQLMovieGenreLink)

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"
engine = create_engine(sqlite_url, echo=True)

def create_db_tables_and_testdata():
	import os
	os.remove(sqlite_file_name)
	SQLModel.metadata.create_all(engine)
	with Session(engine) as session:
		gAction = Genere(tag="Action")
		gAnimation = Genere(tag="Animation")
		gAdventure = Genere(tag="Adventure")
		gComedy = Genere(tag="Comedy")
		gCrime = Genere(tag="Crime")
		gDrama = Genere(tag="Drama")
		gHorror = Genere(tag="Horror")
		gSci = Genere(tag="Sci-Fi")
		gThriller = Genere(tag="Thriller")
		session.add(SQLMovie(m_id="tt0944835", title="Salt", rating=6.4, release_year=2010, generes=[gAction, gThriller]))
		session.add(SQLMovie(m_id="tt0314006", title="Dum", rating=5.6, release_year=2003, generes=[gAction, gCrime, gDrama]))
		session.add(SQLMovie(m_id="tt0397892", title="Bolt", rating=6.8, release_year=2008, generes=[gAnimation, gAdventure, gComedy]))
		session.add(SQLMovie(m_id="tt2316204", title="Alien: Covenant", rating=6.4, release_year=2017, generes=[gHorror, gSci, gThriller]))
		session.add(SQLMovie(m_id="tt0422091", title="Dhoom", rating=6.7, release_year=2004, generes=[gAction, gCrime, gDrama]))
		session.add(SQLMovie(m_id="tt0441048", title="Dhoom 2", rating=6.6, release_year=2006, generes=[gAction, gCrime, gThriller]))
		session.commit()
	return

def insert_new_movie(fetched_movie: Movie):
	with Session(engine) as session:
		known_G = session.exec(select(Genere)).all()
		unknown_generes = set(fetched_movie.genere) - {getattr(el, 'tag') for el in known_G}
		new_G = [Genere(tag=el) for el in fetched_movie.genere] if unknown_generes else []
		existing_G = [el for el in known_G if el.tag in fetched_movie.genere]
		insertable = SQLMovie(
			m_id=fetched_movie.m_id,
			title=fetched_movie.title,
			rating=fetched_movie.rating,
			release_year=fetched_movie.release_year,
			generes=existing_G + new_G
		)
		session.add(insertable)
		session.commit()
	return

def model_to_json(movie_id: str) -> Movie:
	with Session(engine) as session:
		match = session.exec(
			select(SQLMovie).where(
				SQLMovie.m_id == movie_id
			)
		).one()
		mglinks = session.exec(
			select(SQLMovieGenreLink).where(
				SQLMovieGenreLink.movie_id == movie_id
			)
		).all()
		generes = [
			session.exec(
				select(Genere).where(Genere.gid == el.genere_id)
			).one_or_none().tag
			for el in mglinks
		]
	return Movie(
		m_id=match.m_id,
		title=match.title,
		rating=match.rating,
		release_year=match.release_year,
		genere=generes
	)

def find_movie(by: str, target: str) -> Optional[Movie]:
	if by not in ["m_id", "title"]:
		return None
	with Session(engine) as session:
		match = session.exec(
			select(SQLMovie).where(getattr(SQLMovie, by) == target)
		).one_or_none()
		if match is None:
			if by == 'title':
				match = fetch(target)
				if match is None:
					return None
				insert_new_movie(match)
			else:
				return None
	return model_to_json(match.m_id)

def find_all_movies(by: str, target: Any) -> List[Movie]:
	matches = list()
	with Session(engine) as session:
		if by == "genere":
			target = session.exec(select(Genere).where(Genere.tag == target)).one().gid
			matches = session.exec(select(SQLMovieGenreLink.movie_id).where(SQLMovieGenreLink.genere_id == target)).all()
		else:
			cmp = operator.ge if by == "rating" else operator.eq
			matches = session.exec(
				select(SQLMovie.m_id).where(
					cmp(getattr(SQLMovie, by), target)
				)
			).all()
	return list(map(model_to_json, matches))
