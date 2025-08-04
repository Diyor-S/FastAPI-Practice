from fastapi import APIRouter, Path
from typing import Annotated

router = APIRouter(prefix="/items", tags=["Items"])


@router.get("/")
def list_items():
    return [
        "item1",
        "item2",
    ]

@router.get("/latest/")
def get_latest_item():
    return {"item": {"id": "0", "name": "latest"}}

# Accepting the ids that are greater than 0
# The new method: 
@router.get("/{item_id}/")
def get_item_by_id(item_id: Annotated[int, Path(gt=0, lt=1_000_000)]):
    return {
        "item": {
            "id": item_id,
        },
    }
    
# The old method: with Path(..., gt=0) ... -> this means required
# @app.get("/items/{item_id}/")
# def get_item_by_id(item_id: int = Path(..., gt=0)):
#     return {
#         "item": {
#             "id": item_id,
#         },
#     }

    