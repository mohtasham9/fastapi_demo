import json
import os
import random
from typing import Literal, Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from mangum import Mangum

# Define a Pydantic model for the Movie
class Movie(BaseModel):
    title: str
    director: str
    year: int
    genre: Literal["fiction", "non-fiction"]

# File path for storing movie data
MOVIES_FILE = "movies.json"
MOVIES = []
# Load movie data from the JSON file
def load_movies():
    if os.path.exists(MOVIES_FILE) and os.path.getsize(MOVIES_FILE) > 0:
        with open(MOVIES_FILE, "r") as f:
            return json.load(f)
    else:
        return MOVIES

# Save movie data to the JSON file
def save_movies(movies):
    with open(MOVIES_FILE, "w") as f:
        json.dump(movies, f, indent=4)

# Initialize FastAPI app
app = FastAPI()

# Initialize Mangum for AWS Lambda
handler = Mangum(app)

# Endpoint to get a random movie
@app.get("/random-movie")
async def random_movie():
    movies = load_movies()
    return random.choice(movies)

# Endpoint to list all movies
@app.get("/list-movies")
async def list_movies():
    return load_movies()

# Endpoint to get a movie by index
@app.get("/movie/{index}")
async def movie_by_index(index: int):
    movies = load_movies()
    if index < len(movies):
        return movies[index]
    else:
        raise HTTPException(status_code=404, detail="Movie not found")

# Endpoint to add a new movie
@app.post("/add-movie")
async def add_movie(movie: Movie):
    movies = load_movies()
    movies.append(movie.dict())
    save_movies(movies)
    return {"message": "Movie added successfully"}

# Endpoint to search for a movie by title
@app.get("/search-movie")
async def search_movie(title: str):
    movies = load_movies()
    result = [movie for movie in movies if title.lower() in movie['title'].lower()]
    if result:
        return result
    else:
        raise HTTPException(status_code=404, detail="Movie not found")

