from typing import List
from django.shortcuts import get_object_or_404
from ninja import Router

from tags.schema import Tag
from tags.models import Tags

router = Router()

# create new tag
@router.post("/", auth=None)
def create_platform(request, payload: Tag):
    tag = Tags.objects.create(**payload.dict())
    return {"id": tag.id}

# get tag by id
@router.get("/id/{id}", response=Tag)
def get_platform_by_id(request, id: str):
    tag_found = False
    try:
        # try regular uuid id
        tag = Tags.objects.filter(id=id).first()
        if tag is not None:
            tag_found = True
    except:
        # try rawg id
        try:
            tag = Tags.objects.filter(rawg_id=id).first()
            if tag is not None:
                tag_found = True
        except:
            return {"Message": "Tag not found"}
            
    if tag_found:
        return tag
    
    return {"Message": "Tag not found"}

# get tag by rawg id
@router.get("/rawg_id/{rawg_id}", response=Tag)
def get_platform_by_rawg_id(request, rawg_id: int):
    tag = get_object_or_404(Tags, rawg_id=rawg_id)
    return tag

# list all tag
@router.get("/", response=List[Tag])
def list_all_platform(request):
    tag_list = Tags.objects.all()[:100]
    return tag_list

# list all tags that contain a str in their title
@router.get("/name/{title_str}", response=List[Tag])
def get_platform_by_name(request, title_str: str):
    tag_list = Tags.objects.filter(name__icontains=title_str)[:100]
    return tag_list

# update tag by id
@router.put("/id/{id}")
def update_platform_by_id(request, id: str, payload: Tag):
    tag_found = False
    try:
        # try regular uuid id
        tag = Tags.objects.filter(id=id).first()
        if tag is not None:
            tag_found = True
    except:
        # try rawg id
        try:
            tag = Tags.objects.filter(rawg_id=id).first()
            if tag is not None:
                tag_found = True
        except:
            return {"Message": "Tag not found"}
            
    if tag_found:
        for attr, value in payload.dict().items():
            setattr(tag, attr, value)
        tag.save()
        return {"success": True}
    else:
        return {"message": "Tag not found"}

# delete/disable tag by id
@router.delete("/id/{id}")
def delete_platform_by_id(request, id: str):
    tag_found = False
    try:
        # try regular uuid id
        tag = Tags.objects.filter(id=id).first()
        if tag is not None:
            tag_found = True
    except:
        # try rawg id
        try:
            tag = Tags.objects.filter(rawg_id=id).first()
            if tag is not None:
                tag_found = True
        except:
            return {"Message": "Tag not found"}
            
    if tag_found:
        tag.enabled = False
        tag.archived = True
        tag.save()
        return {"success": True}
    else:
        return {"Message": "Tag not found"}

# delete/disable tag by rawg id
@router.delete("/rawg_id/{rawg_id}")
def delete_platform_by_rawg_id(request, rawg_id: int):
    tag = get_object_or_404(Tags, rawg_id=rawg_id)
    tag.enabled = False
    tag.archived = True
    tag.save()
    return {"success": True}

###################################
# HELPERS
###################################