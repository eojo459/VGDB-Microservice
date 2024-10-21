from typing import List
from django.shortcuts import get_object_or_404
from ninja import Router

from stores.schema import Store
from stores.models import Stores

router = Router()

# create new store
@router.post("/", auth=None)
def create_platform(request, payload: Store):
    store = Stores.objects.create(**payload.dict())
    return {"id": store.id}

# get store by id
@router.get("/id/{id}", response=Store)
def get_platform_by_id(request, id: str):
    store_found = False
    try:
        # try regular uuid id
        store = Stores.objects.filter(id=id).first()
        if store is not None:
            store_found = True
    except:
        # try rawg id
        try:
            store = Stores.objects.filter(rawg_id=id).first()
            if store is not None:
                store_found = True
        except:
            return {"Message": "Store not found"}
            
    if store_found:
        return store
    
    return {"Message": "Store not found"}

# get store by rawg id
@router.get("/rawg_id/{rawg_id}", response=Store)
def get_platform_by_rawg_id(request, rawg_id: int):
    store = get_object_or_404(Stores, rawg_id=rawg_id)
    return store

# list all store
@router.get("/", response=List[Store])
def list_all_platform(request):
    store_list = Stores.objects.all()[:100]
    return store_list

# list all stores that contain a str in their title
@router.get("/name/{title_str}", response=List[Store])
def get_platform_by_name(request, title_str: str):
    store_list = Stores.objects.filter(name__icontains=title_str)[:100]
    return store_list

# update store by id
@router.put("/id/{id}")
def update_platform_by_id(request, id: str, payload: Store):
    store_found = False
    try:
        # try regular uuid id
        store = Stores.objects.filter(id=id).first()
        if store is not None:
            store_found = True
    except:
        # try rawg id
        try:
            store = Stores.objects.filter(rawg_id=id).first()
            if store is not None:
                store_found = True
        except:
            return {"Message": "Store not found"}
            
    if store_found:
        for attr, value in payload.dict().items():
            setattr(store, attr, value)
        store.save()
        return {"success": True}
    else:
        return {"message": "Store not found"}

# delete/disable store by id
@router.delete("/id/{id}")
def delete_platform_by_id(request, id: str):
    store_found = False
    try:
        # try regular uuid id
        store = Stores.objects.filter(id=id).first()
        if store is not None:
            store_found = True
    except:
        # try rawg id
        try:
            store = Stores.objects.filter(rawg_id=id).first()
            if store is not None:
                store_found = True
        except:
            return {"Message": "Store not found"}
            
    if store_found:
        store.enabled = False
        store.archived = True
        store.save()
        return {"success": True}
    else:
        return {"Message": "Store not found"}

# delete/disable store by rawg id
@router.delete("/rawg_id/{rawg_id}")
def delete_platform_by_rawg_id(request, rawg_id: int):
    store = get_object_or_404(Stores, rawg_id=rawg_id)
    store.enabled = False
    store.archived = True
    store.save()
    return {"success": True}

###################################
# HELPERS
###################################