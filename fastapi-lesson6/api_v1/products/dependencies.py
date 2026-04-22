from fastapi import Path, HTTPException, status, Depends
from typing import Annotated
from api_v1.products import crud
from sqlalchemy.ext.asyncio import AsyncSession
from core.models import db_helper, Product


async def get_product_by_id(
    session: Annotated[AsyncSession, Depends(db_helper.session_dependency)],
    product_id: Annotated[int, Path],
) -> Product:
    product = await crud.get_product(session=session, product_id=product_id)

    if product is not None:
        return product

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"Product {product_id} not found!"
    )
