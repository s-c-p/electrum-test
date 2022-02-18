from typing import List
from pydantic import BaseModel

class Movie(BaseModel):
	m_id: str
	title: str
	rating: float
	release_year: int
	genere: List[str]

