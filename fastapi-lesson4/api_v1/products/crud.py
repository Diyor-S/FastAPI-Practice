from api_v1.products import ProductUpdatePartial
from core.models import Product
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.engine import Result
from api_v1.products import ProductCreate, ProductUpdate


async def create_product(session: AsyncSession, product: ProductCreate) -> Product:
    new_product = Product(**product.model_dump())
    session.add(new_product)
    await session.commit()
    await session.refresh(new_product)
    return new_product


async def get_products(session: AsyncSession) -> list[Product]:
    stmt = select(Product).order_by(Product.id)
    result: Result = await session.execute(stmt)
    products = result.scalars().all()
    return list(products)


async def get_product(session: AsyncSession, product_id: int) -> Product | None:
    return await session.get(Product, product_id)


# Implementation of Put
# async def update_product(
#     session: AsyncSession, product: Product, updated_product: ProductUpdate
# ) -> Product:

#     for name, value in updated_product.model_dump().items():
#         setattr(product, name, value)

#     await session.commit()
#     return product

# Implementation of Patch
# async def update_product_partial(
#     session: AsyncSession,
#     product: Product,
#     partially_update_product: ProductUpdatePartial,
# ) -> Product:

#     for name, value in partially_update_product.model_dump(
#         exclude_unset=True, exclude_none=True
#     ).items():
#         setattr(product, name, value)
#     await session.commit()
#     return product


# Combination of both Put and Patch:
async def update_product(
    session: AsyncSession,
    product: Product,
    updated_product: ProductUpdate | ProductUpdatePartial,
    partial: bool = False,
) -> Product:

    for name, value in updated_product.model_dump(exclude_unset=partial).items():
        setattr(product, name, value)

    await session.commit()
    return product


async def delete_product(session: AsyncSession, product: Product) -> None:
    await session.delete(product)
    await session.commit()
