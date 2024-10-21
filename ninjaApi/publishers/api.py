from typing import List
from django.shortcuts import get_object_or_404
from ninja import Router
from decouple import config
import requests
from ninjaApi.backendApi.utils.helper import calculate_day_difference
from ninjaApi.publishers.models import Publishers
from ninjaApi.publishers.schema import Publisher
from platforms.schema import Platform
from platforms.models import Platforms

router = Router()


### initial seeding ##
@router.get("/seeding/")
def publishers_seeding(request):
    fetch_publishers_RAWG()
    return {"success": True}

# create new publisher
@router.post("/", auth=None)
def create_publisher(request, payload: Publisher):
    publisher = Publishers.objects.create(**payload.dict())
    return {"id": publisher.id}

# get publisher by id
@router.get("/id/{id}", response=Publisher)
def get_publisher_by_id(request, id: str):
    publisher_found = False
    try:
        # try regular uuid id
        publisher = Publishers.objects.filter(id=id).first()
        if publisher is not None:
            publisher_found = True
    except:
        # try rawg id
        try:
            publisher = Publishers.objects.filter(rawg_id=id).first()
            if publisher is not None:
                publisher_found = True
        except:
            return {"Message": "Publisher not found"}
            
    if publisher_found:
        return publisher
    
    return {"Message": "Publisher not found"}

# get publisher by rawg id
@router.get("/rawg_id/{rawg_id}", response=Publisher)
def get_publisher_by_rawg_id(request, rawg_id: int):
    publisher = get_object_or_404(Publishers, rawg_id=rawg_id)
    return publisher

# list all publisher
@router.get("/", response=List[Publisher])
def list_all_publisher(request):
    publisher_list = Publishers.objects.all()[:100]
    return publisher_list

# list all publishers that contain a str in their title
@router.get("/name/{title_str}", response=List[Publisher])
def get_publisher_by_name(request, title_str: str):
    publisher_list = Publishers.objects.filter(name__icontains=title_str)[:100]
    return publisher_list

# update publisher by id
@router.put("/id/{id}")
def update_publisher_by_id(request, id: str, payload: Publisher):
    publisher_found = False
    try:
        # try regular uuid id
        publisher = Publishers.objects.filter(id=id).first()
        if publisher is not None:
            publisher_found = True
    except:
        # try rawg id
        try:
            publisher = Publishers.objects.filter(rawg_id=id).first()
            if publisher is not None:
                publisher_found = True
        except:
            return {"Message": "Publisher not found"}
            
    if publisher_found:
        for attr, value in payload.dict().items():
            setattr(publisher, attr, value)
        publisher.save()
        return {"success": True}
    else:
        return {"message": "Publisher not found"}

# delete/disable publisher by id
@router.delete("/id/{id}")
def delete_publisher_by_id(request, id: str):
    publisher_found = False
    try:
        # try regular uuid id
        publisher = Publishers.objects.filter(id=id).first()
        if publisher is not None:
            publisher_found = True
    except:
        # try rawg id
        try:
            publisher = Publishers.objects.filter(rawg_id=id).first()
            if publisher is not None:
                publisher_found = True
        except:
            return {"Message": "Publisher not found"}
            
    if publisher_found:
        publisher.enabled = False
        publisher.archived = True
        publisher.save()
        return {"success": True}
    else:
        return {"Message": "Publisher not found"}

# delete/disable publisher by rawg id
@router.delete("/rawg_id/{rawg_id}")
def delete_publisher_by_rawg_id(request, rawg_id: int):
    publisher = get_object_or_404(Publishers, rawg_id=rawg_id)
    publisher.enabled = False
    publisher.archived = True
    publisher.save()
    return {"success": True}

###################################
# HELPERS
###################################

# get publishers from RAWG
def fetch_publishers_RAWG():
    base_url = config('RAWG_BASE_URL') + "publishers" + "?key=" + config('RAWG_API_KEY')
    page = 1

    url = f"{base_url}&page={page}"
    response = requests.get(url)
    response_json = response.json()

    # get all the pages we can get
    while response_json['next'] is not None:
        print("===== Page " + str(page) + " =====")

        # for each result on this page, create new publisher entry in database if doesn't already exist
        for result in response_json['results']:

            # create publisher info
            publisher_info = {
                'rawg_id': result['id'],
                'slug': result['slug'],
                'name': result['name'],
                'games_count': result['games_count'],
                'background_image': result['background_image'],
            }

            # check if publisher doesn't already exist
            publisher_exists = Publishers.objects.filter(rawg_id=result['id']).first()
            if publisher_exists and publisher_exists.last_updated is not None:
                if calculate_day_difference(publisher_exists.last_updated.strftime('%Y-%m-%d'), 7):
                    # update publisher entry
                    publisher_exists.games_count = result['games_count']
                    publisher_exists.save()
            elif publisher_exists is None:
                # create new game entry
                new_publisher = Publishers.objects.create(**publisher_info)
            else:
                continue # skip

        # go to next page
        page += 1
        response = requests.get(response_json['next'])
        response_json = response.json()

    return True