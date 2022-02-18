# electrum-test

To implement an API for movie search on IMDb database. Caching is key to endpoint split. For full details see problem statement verbatim in PDF file (email attachment) with SHA1 8be98cfbf856fbd60e569174e01f71302dd841ba.

### Following is a list of deliverables I see:

Make API to search a movie by

 * id -> Movie
 * title (exact) -> Movie

  > if no match in localDB, call omdbapi, if 2xx reply store in localDB, else discard

 * year -> List[Movie]
 * minimum_rating -> List[Movie]
 * genere -> List[Movie]

Shape of data:

 * title - str
 * released year - +ve int, 4 digit, sensible?
 * rating - float (0,5]
 * id - str, alphanumeric
 * genere - List[str]

### Freedoms:

 * no mention of DB technology, for 0.0.1 release I'll use in-memory dict (anyway free API limit is 1000/day so it's unlikely to flood RAM in first day), persistance via plain-JSON/shelve, mean #tags per movie is small indexing of 1-to-many isn't a concern for current size of dataset
 * no mention of libraries, I'll use bottle/FastAPI, collections.NamedTuple/pydantic
