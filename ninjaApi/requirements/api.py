from typing import List
from django.shortcuts import get_object_or_404
from ninja import Router
from requirements.models import Requirements
from requirements.schema import Requirement


router = Router()

# create new requirements
@router.post("/", auth=None)
def create_requirement(request, payload: Requirement):
    requirement = Requirements.objects.create(**payload.dict())
    return {"id": requirement.id}

# get requirement by id
@router.get("/id/{id}", response=Requirement)
def get_requirement_by_id(request, id: str):
    requirement_found = False
    try:
        # try regular uuid id
        requirement = Requirements.objects.filter(id=id).first()
        if requirement is not None:
            requirement_found = True
    except:
        # try rawg id
        try:
            requirement = Requirements.objects.filter(rawg_id=id).first()
            if requirement is not None:
                requirement_found = True
        except:
            return {"Message": "Requirement not found"}
            
    if requirement_found:
        return requirement
    
    return {"Message": "Requirement not found"}

# get requirement by rawg id
@router.get("/rawg_id/{rawg_id}", response=Requirement)
def get_requirement_by_rawg_id(request, rawg_id: int):
    requirement = get_object_or_404(Requirements, rawg_id=rawg_id)
    return requirement

# list all requirements
@router.get("/", response=List[Requirement])
def list_all_requirements(request):
    requirement_list = Requirements.objects.all()[:100]
    return requirement_list

# list all requirements that contain a str in their title
@router.get("/name/{title_str}", response=List[Requirement])
def get_requirement_by_name(request, title_str: str):
    requirement_list = Requirements.objects.filter(name__icontains=title_str)[:100]
    return requirement_list

# update requirement by id
@router.put("/id/{id}")
def update_requirement_by_id(request, id: str, payload: Requirement):
    requirement_found = False
    try:
        # try regular uuid id
        requirement = Requirements.objects.filter(id=id).first()
        if requirement is not None:
            requirement_found = True
    except:
        # try rawg id
        try:
            requirement = Requirements.objects.filter(rawg_id=id).first()
            if requirement is not None:
                requirement_found = True
        except:
            return {"Message": "Requirement not found"}
            
    if requirement_found:
        for attr, value in payload.dict().items():
            setattr(requirement, attr, value)
        requirement.save()
        return {"success": True}
    else:
        return {"message": "Requirement not found"}

# delete/disable requirement by id
@router.delete("/id/{id}")
def delete_requirement_by_id(request, id: str):
    requirement_found = False
    try:
        # try regular uuid id
        requirement = Requirements.objects.filter(id=id).first()
        if requirement is not None:
            requirement_found = True
    except:
        # try rawg id
        try:
            requirement = Requirements.objects.filter(rawg_id=id).first()
            if requirement is not None:
                requirement_found = True
        except:
            return {"Message": "Requirement not found"}
            
    if requirement_found:
        requirement.enabled = False
        requirement.archived = True
        requirement.save()
        return {"success": True}
    else:
        return {"Message": "Requirement not found"}

# delete/disable requirement by rawg id
@router.delete("/rawg_id/{rawg_id}")
def delete_requirement_by_rawg_id(request, rawg_id: int):
    requirement = get_object_or_404(Requirements, rawg_id=rawg_id)
    requirement.enabled = False
    requirement.archived = True
    requirement.save()
    return {"success": True}

###################################
# HELPERS
###################################