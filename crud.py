import asyncio
from sqlalchemy import Result, select
from sqlalchemy.orm import joinedload, selectinload

# from sqlalchemy import Result
from sqlalchemy.ext.asyncio import AsyncSession
from core.models import db_helper, User, Profile, Post


async def create_user(session: AsyncSession, username: str) -> User:
    user = User(username=username)
    session.add(user)
    await session.commit()
    print("user:", user)
    return user


async def get_user_by_username(session: AsyncSession, username: str) -> User:
    stmt = select(User).where(User.username == username)

    # Instead of this:
    result: Result = await session.execute(stmt)
    # user: User | None = result.scalar_one_or_none()

    # We can do this:
    user: User = result.scalar_one()

    print("Found user:", username, user)
    return user


async def create_user_profile(
    session: AsyncSession,
    user_id: int,
    first_name: str | None = None,
    last_name: str | None = None,
) -> Profile:
    profile = Profile(
        user_id=user_id,
        first_name=first_name,
        last_name=last_name,
    )
    session.add(profile)
    await session.commit()
    return profile


async def show_users_with_profiles(session: AsyncSession):
    stmt = select(User).options(joinedload(User.profile)).order_by(User.id)
    users = await session.scalars(stmt)
    for user in users:
        print("For user:", user)
        print("Profile: ")
        print("--", user.profile.first_name)


async def create_posts(
    session: AsyncSession,
    user_id: int,
    *post_titles: str,
) -> list[Post]:
    posts = [Post(title=title, user_id=user_id) for title in post_titles]
    session.add_all(posts)
    await session.commit()
    print(posts)
    return posts


async def get_users_with_posts(
    session: AsyncSession,
):
    stmt = select(User).options(selectinload(User.posts)).order_by(User.id)
    users = await session.scalars(stmt)
    for user in users:
        print("**" * 30)
        print(user)
        print("\tPosts:")
        if user.posts:
            for post in user.posts:
                print(f"\t\t{post}")
        else:
            print("\t\tNo posts")


async def get_posts_with_users(session: AsyncSession):
    stmt = select(Post).options(joinedload(Post.user)).order_by(Post.id)
    posts = await session.scalars(stmt)

    for post in posts:
        print(f"Post: {post}")
        print(f"\tUser: {post.user}")


async def get_users_with_profiles_and_posts(session: AsyncSession):
    stmt = (
        select(User)
        .options(joinedload(User.profile), selectinload(User.posts))
        .order_by(User.id)
    )
    users = await session.scalars(stmt)

    for user in users:
        print("***" * 30)
        print("User:", user)
        if user.profile:
            print(f"\t{user.username}'s profile: {user.profile}")
        else:
            print(f"\t{user.username}'s profile: No profile found!")

        if user.posts:
            print(f"\t\t{user.username}'s posts: ")
            for post in user.posts:
                print("\t\t\t", post)
        else:
            print(f"\t\t{user.username}'s posts: No posts found!")


async def get_profiles_with_users_and_users_with_posts(session: AsyncSession):
    stmt = (
        select(Profile)
        .join(Profile.user)  # this join for filtering
        .options(
            joinedload(Profile.user).selectinload(User.posts)
        )  # joinedload for data retrieval
        .where(User.username == "sam")
        .order_by(Profile.id)
    )

    profiles = await session.scalars(stmt)

    for profile in profiles:
        print("***" * 30)
        print("Profile:", profile)
        if profile.user:
            print(f"\t{profile.first_name} profile's user: {profile.user}")
        else:
            print(f"\t{profile.first_name} profile's user: No user found!")

        print(f"\t\t{profile.user.username}'s posts: ")
        if profile.user.posts:
            for post in profile.user.posts:
                print("\t\t\t--", post)
        else:
            print("\t\t\t--No posts found!")


async def main():
    async with db_helper.session_factory() as session:
        # await create_user(session=session, username="john")
        # await create_user(session=session, username="sam")
        # await create_user(session=session, username="alice")

        # user_john = await get_user_by_username(session=session, username="john")
        # user_sam = await get_user_by_username(session=session, username="sam")
        # user_alice = await get_user_by_username(session=session, username="alice")
        # await create_user_profile(
        #     session=session,
        #     user_id=user_john.id,
        #     first_name="John",
        # )
        # await create_user_profile(
        #     session=session, user_id=user_sam.id, first_name="Sam", last_name="White"
        # )

        # await show_users_with_profiles(session=session)
        # await create_posts(
        #     session,
        #     user_john.id,
        #     *["SQLA 2.0", "SQL Joins"],
        # )

        # await create_posts(
        #     session,
        #     user_sam.id,
        #     *["Fast API Intro", "Fast API Advanced"],
        # )

        # await create_posts(
        #     session,
        #     user_alice.id,
        # )
        # await get_users_with_posts(session=session)
        # await get_posts_with_users(session)
        # await get_users_with_profiles_and_posts(session)
        await get_profiles_with_users_and_users_with_posts(session)


if __name__ == "__main__":
    asyncio.run(main())
