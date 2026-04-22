from fastapi import APIRouter, Depends, status
from api_v1.products import crud
from api_v1.products.schemas import (
    Product,
    ProductCreate,
    ProductUpdate,
    ProductUpdatePartial,
)
from api_v1.products.dependencies import get_product_by_id
from core.models import db_helper, Product as ProductORM
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession


router = APIRouter(tags=["Products"])


@router.post("/", response_model=Product, status_code=status.HTTP_201_CREATED)
async def create_product(
    session: Annotated[AsyncSession, Depends(db_helper.session_dependency)],
    product: ProductCreate,
):
    return await crud.create_product(session=session, product=product)


@router.get("/", response_model=list[Product])
async def get_all_products(
    session: Annotated[AsyncSession, Depends(db_helper.session_dependency)],
):
    return await crud.get_products(session=session)


@router.get("/{product_id}/", response_model=Product)
async def get_product(product: Annotated[ProductORM, Depends(get_product_by_id)]):
    return product


@router.put("/{product_id}/", response_model=Product)
async def update_product(
    session: Annotated[AsyncSession, Depends(db_helper.session_dependency)],
    product: Annotated[ProductORM, Depends(get_product_by_id)],
    updated_product: ProductUpdate,
):
    return await crud.update_product(
        session=session, product=product, updated_product=updated_product
    )


@router.patch("/{product_id}/", response_model=Product)
async def update_product_partial(
    session: Annotated[AsyncSession, Depends(db_helper.session_dependency)],
    product: Annotated[ProductORM, Depends(get_product_by_id)],
    update_product: ProductUpdatePartial,
):
    return await crud.update_product(
        session=session, product=product, updated_product=update_product, partial=True
    )


@router.delete("/{product_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(
    session: Annotated[AsyncSession, Depends(db_helper.session_dependency)],
    product: Annotated[ProductORM, Depends(get_product_by_id)],
) -> None:
    return await crud.delete_product(session=session, product=product)
