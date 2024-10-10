from typing import List
from django.shortcuts import get_object_or_404
from ninja import Router

from platforms.schema import Platform
from platforms.models import Platforms

router = Router()

# create new platform
@router.post("/", auth=None)
def create_platform(request, payload: Platform):
    platform = Platforms.objects.create(**payload.dict())
    return {"id": platform.id}

# get platform by id
@router.get("/id/{id}", response=Platform)
def get_platform_by_id(request, id: str):
    platform_found = False
    try:
        # try regular uuid id
        platform = Platforms.objects.filter(id=id).first()
        if platform is not None:
            platform_found = True
    except:
        # try rawg id
        try:
            platform = Platforms.objects.filter(rawg_id=id).first()
            if platform is not None:
                platform_found = True
        except:
            return {"Message": "Platform not found"}
            
    if platform_found:
        return platform
    
    return {"Message": "Platform not found"}

# get platform by rawg id
@router.get("/rawg_id/{rawg_id}", response=Platform)
def get_platform_by_rawg_id(request, rawg_id: int):
    platform = get_object_or_404(Platforms, rawg_id=rawg_id)
    return platform

# list all platform
@router.get("/", response=List[Platform])
def list_all_platform(request):
    platform_list = Platforms.objects.all()[:100]
    return platform_list

# list all platforms that contain a str in their title
@router.get("/name/{title_str}", response=List[Platform])
def get_platform_by_name(request, title_str: str):
    platform_list = Platforms.objects.filter(name__icontains=title_str)[:100]
    return platform_list

# update platform by id
@router.put("/id/{id}")
def update_platform_by_id(request, id: str, payload: Platform):
    platform_found = False
    try:
        # try regular uuid id
        platform = Platforms.objects.filter(id=id).first()
        if platform is not None:
            platform_found = True
    except:
        # try rawg id
        try:
            platform = Platforms.objects.filter(rawg_id=id).first()
            if platform is not None:
                platform_found = True
        except:
            return {"Message": "Platform not found"}
            
    if platform_found:
        for attr, value in payload.dict().items():
            setattr(platform, attr, value)
        platform.save()
        return {"success": True}
    else:
        return {"message": "Platform not found"}

# delete/disable platform by id
@router.delete("/id/{id}")
def delete_platform_by_id(request, id: str):
    platform_found = False
    try:
        # try regular uuid id
        platform = Platforms.objects.filter(id=id).first()
        if platform is not None:
            platform_found = True
    except:
        # try rawg id
        try:
            platform = Platforms.objects.filter(rawg_id=id).first()
            if platform is not None:
                platform_found = True
        except:
            return {"Message": "Platform not found"}
            
    if platform_found:
        platform.enabled = False
        platform.archived = True
        platform.save()
        return {"success": True}
    else:
        return {"Message": "Platform not found"}

# delete/disable platform by rawg id
@router.delete("/rawg_id/{rawg_id}")
def delete_platform_by_rawg_id(request, rawg_id: int):
    platform = get_object_or_404(Platforms, rawg_id=rawg_id)
    platform.enabled = False
    platform.archived = True
    platform.save()
    return {"success": True}

###################################
# HELPERS
###################################