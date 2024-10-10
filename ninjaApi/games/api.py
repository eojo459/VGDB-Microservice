from django.forms import model_to_dict
import requests
from datetime import date, datetime
from typing import List
from uuid import UUID
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from ninja import Router, Schema
from genres.api import Genre, GenreOut
from backendApi.utils.helper import calculate_day_difference
from genres.models import Genres
from games.schema import Game
from games.models import Games
from platforms.models import Platforms
from requirements.models import Requirements
from decouple import config

router = Router()



################################
# API CONTROLLER METHODS
################################

### initial seeding ##
@router.get("/seeding/")
def games_seeding(request):
    fetch_games_RAWG()
    return {"success": True}
   #return response.json()

# create new game
@router.post("/", auth=None)
def create_game(request, payload: Game):
    game = Games.objects.create(**payload.dict())
    return {"id": game.id}

# get game by id
@router.get("/id/{id}", response=Game)
def get_game_by_id(request, id: str):
    game_found = False
    try:
        # try regular uuid id
        game = Games.objects.prefetch_related(
            'platforms',
            'requirements',
        ).filter(id=id).first()
        if game is not None:
            game_found = True
    except:
        # try rawg id
        try:
            game = Games.objects.prefetch_related(
                'platforms',
                'requirements',
            ).filter(rawg_id=id).first()
            if game is not None:
                game_found = True
        except:
            return {"Message": "Game not found"}
            
    if game_found:
        return game
    
    return {"Message": "Game not found"}

# get game by rawg id
@router.get("/rawg_id/{rawg_id}", response=Game)
def get_game_by_rawg_id(request, rawg_id: int):
    game = get_object_or_404(Games, rawg_id=rawg_id)
    return game

# list all games
@router.get("/", response=List[Game])
def list_all_games(request):
    games_list = Games.objects.prefetch_related(
        'platforms',
        'requirements',
    ).all()[:100]
    return games_list

# list all games that contain a str in their title
@router.get("/name/{title_str}", response=List[Game])
def get_games_by_name(request, title_str: str):
    games_list = Games.objects.prefetch_related(
        'platforms',
        'requirements',
    ).filter(title__icontains=title_str)[:100]
    return games_list

# update game by id
@router.put("/id/{id}")
def update_game_by_id(request, id: str, payload: Game):
    game_found = False
    try:
        # try regular uuid id
        game = Games.objects.filter(id=id).first()
        if game is not None:
            game_found = True
    except:
        # try rawg id
        try:
            game = Games.objects.filter(rawg_id=id).first()
            if game is not None:
                game_found = True
        except:
            return {"Message": "Game not found"}
            
    if game_found:
        for attr, value in payload.dict().items():
            setattr(game, attr, value)
        game.save()
        return {"success": True}
    else:
        return {"message": "Game not found"}

# delete/disable game by id
@router.delete("/id/{id}")
def delete_game_by_id(request, id: str):
    game_found = False
    try:
        # try regular uuid id
        game = Games.objects.filter(id=id).first()
        if game is not None:
            game_found = True
    except:
        # try rawg id
        try:
            game = Games.objects.filter(rawg_id=id).first()
            if game is not None:
                game_found = True
        except:
            return {"Message": "Game not found"}
            
    if game_found:
        game.enabled = False
        game.archived = True
        game.save()
        return {"success": True}
    else:
        return {"Message": "Game not found"}

# delete/disable game by rawg id
@router.delete("/rawg_id/{rawg_id}")
def delete_game_by_tmdb_id(request, rawg_id: int):
    game = get_object_or_404(Games, rawg_id=rawg_id)
    game.enabled = False
    game.archived = True
    game.save()
    return {"success": True}

###################################
# HELPERS
###################################

# get games from RAWG
def fetch_games_RAWG():
    base_url = config('RAWG_BASE_URL') + "games" + "?key=" + config('RAWG_API_KEY')
    page = 1

    url = f"{base_url}&page={page}"
    response = requests.get(url)
    response_json = response.json()

    # get all the pages we can get
    while response_json['next'] is not None:
        print("===== Page " + str(page) + " =====")

        # for each result on this page, create new game entry in database if doesn't already exist
        for result in response_json['results']:

            # create game info
            game_info = {
                'rawg_id': result['id'],
                'slug': result['slug'],
                'name': result['name'],
                'released': result['released'],
                'tba': result['tba'],
                'rating': result['rating'],
                'bg_image': result['background_image'],
                'ratings_count': result['ratings_count'],
                'reviews_text_count': result['reviews_text_count'],
                'metacritic': result['metacritic'],
                'playtime': result['playtime'],
            }

            # check if game doesn't already exist
            game_exists = Games.objects.filter(rawg_id=result['id']).first()
            current_game = None
            if game_exists and game_exists.last_updated is not None:
                current_game = game_exists
                if calculate_day_difference(game_exists.last_updated.strftime('%Y-%m-%d'), 7):
                    # update game entry
                    game_exists.rating = result['rating']
                    game_exists.rating_top = result['rating_top']
                    game_exists.ratings_count = result['rating_count']
                    game_exists.metacritic = result['metacritic']
                    game_exists.tba = result['tba']
                    game_exists.save()
            elif game_exists is None:
                # create new game entry
                new_game = Games.objects.create(**game_info)
                current_game = new_game
                #new_game.platforms.set(platform_list_fk)
                #new_game.save()
            else:
                continue # skip

            # get each platform
            platform_list = []
            requirement_list = []
            for platform in result['platforms']:
                if platform['requirements_en'] is not None:
                    if 'minimum' in platform['requirements_en']:
                        minimum_requirements = platform['requirements_en']['minimum']
                    else:
                        minimum_requirements = None

                    if 'recommended' in platform['requirements_en']:
                        recommended_requirements = platform['requirements_en']['recommended']
                    else:
                        recommended_requirements = None
                else:
                    minimum_requirements = None
                    recommended_requirements = None

                platform_info = {
                    'rawg_id': platform['platform']['id'],
                    'name': platform['platform']['name'],
                    'slug': platform['platform']['slug'],
                }

                # check if platform already exists
                platform_exists = Platforms.objects.filter(rawg_id=platform['platform']['id']).first()
                current_platform = None
                if platform_exists is None:
                    new_platform = Platforms.objects.create(**platform_info)
                    current_platform = new_platform
                else:
                    current_platform = platform_exists

                platform_list.append(current_platform)

                if minimum_requirements is not None or recommended_requirements is not None:
                    requirement_info = {
                        'name': platform_info['name'],
                        'minimum_requirements': minimum_requirements,
                        'recommended_requirements': recommended_requirements,
                    }

                    # check if requirement already exists
                    requirement_exists = Requirements.objects.filter(name=platform_info['name'], 
                                                                     game=current_game).first()
                    current_requirement = None
                    if requirement_exists is None:
                        new_requirement = Requirements.objects.create(**requirement_info)
                        new_requirement.platform.set([current_platform])
                        new_requirement.game.set([current_game])
                        current_requirement = new_requirement
                    else:
                        current_requirement = requirement_exists

                    requirement_list.append(current_requirement)

            current_game.platforms.set(platform_list)
            current_game.requirements.set(requirement_list)
            current_game.save()
                
            

        # go to next page
        page += 1
        response = requests.get(response_json['next'])
        response_json = response.json()

    return True