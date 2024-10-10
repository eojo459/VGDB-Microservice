from datetime import date, datetime
from typing import List
from uuid import UUID
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from ninja import Router, Schema
import requests
from genres.models import Genres
from decouple import config
from genres.schema import GenreOut, Genre
from backendApi.utils.helper import calculate_day_difference

router = Router()

################################
# API CONTROLLER METHODS
################################

### initial seeding ##
@router.get("/seeding/")
def fetch_genres_RAWG():
    base_url = config('RAWG_BASE_URL') + "genres" + "?key=" + config('RAWG_API_KEY')
    page = 1

    url = f"{base_url}&page={page}"
    response = requests.get(url)
    response_json = response.json()

    # for each result on this page, create new movie entry in database if doesn't already exist
    for result in response_json['results']:
            
        # create genre info
        genre_info = {
            'rawg_id': result['id'],
            'slug': result['slug'],
            'name': result['name'],
            'games_count': result['games_count'],
        }

        # check if genre doesn't already exist
        genre_exists = Genres.objects.filter(tmdb_id=result['id']).first()
        if genre_exists and genre_exists.last_updated is not None:
            if calculate_day_difference(genre_exists.last_updated.strftime('%Y-%m-%d'), 7):
                # update genre entry
                genre_exists.games_count = result['games_count']
                genre_exists.save()
        elif genre_exists is None:
            # create new game entry
            new_genre = Genres.objects.create(**genre_info)
        else:
            continue # skip

    return True
    
# create new genre
@router.post("/", auth=None)
def create_genre(request, payload: Genre):
    genre = Genres.objects.create(**payload.dict())
    return {"id": genre.id}

# get genre by id
@router.get("/id/{id}", response=GenreOut)
def get_genre_by_id(request, id: str):
    genre = get_object_or_404(Genres, id=id)
    return genre

# get genre by rawg id
@router.get("/rawg_id/{rawg_id}", response=GenreOut)
def get_genre_by_rawg_id(request, rawg_id: int):
    genre = get_object_or_404(Genres, rawg_id=rawg_id)
    return genre

# list all genres
@router.get("/", response=List[GenreOut])
def list_all_genres(request):
    genre_list = Genres.objects.all()
    return genre_list

# update genre by id
@router.put("/id/{id}")
def update_genre_by_id(request, id: str, payload: GenreOut):
    genre = get_object_or_404(Genres, id=id)
    for attr, value in payload.dict().items():
        setattr(genre, attr, value)
    genre.save()
    return {"success": True}

# update genre by rawg id
@router.put("/rawg_id/{rawg_id}")
def update_genre_by_rawg_id(request, rawg_id: int, payload: GenreOut):
    genre = get_object_or_404(Genres, rawg_id=rawg_id)
    for attr, value in payload.dict().items():
        setattr(genre, attr, value)
    genre.save()
    return {"success": True}

# delete/disable genre by id
@router.delete("/id/{id}")
def delete_genre_by_id(request, id: str):
    genre = get_object_or_404(Genres, id=id)
    #genre.delete()
    genre.enabled = False
    genre.archived = True
    genre.save()
    return {"success": True}

# delete/disable genre by rawg id
@router.delete("/rawg_id/{rawg_id}")
def delete_genre_by_rawg_id(request, rawg_id: int):
    genre = get_object_or_404(Genres, rawg_id=rawg_id)
    #genre.delete()
    genre.enabled = False
    genre.archived = True
    genre.save()
    return {"success": True}