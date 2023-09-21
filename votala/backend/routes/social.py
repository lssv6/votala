""""""
from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy import Engine

from dependencies.authentication import get_current_user
from dependencies.database import get_engine
from models.custom_responses import ServerMessage
from models.schemas import *
from modules.social import *

social_groups = APIRouter(tags=["social", "groups"], prefix="/groups")
social_users = APIRouter(tags=["social", "users"], prefix="/users")

###############################################################################


@social_groups.post("", name="Create a new group")
def post_group(
    group_to_create: GroupCreate,
    creator: User = Depends(get_current_user),
    engine: Engine = Depends(get_engine),
):
    """Create a new group"""
    with Session(engine) as session:
        create_group(session, creator, group_to_create)


###############################################################################
@social_groups.get(
    "/{group_id}",
    name="Get group data",
    response_model=Optional[Group],
    responses={
        200: {"model": Group, "description": "The main data about a group."},
        404: {"model": ServerMessage, "description": "The given group doesn't exists."},
    },
)
def get_group_endpoint(group_id: str, engine: Engine = Depends(get_engine)):
    with Session(engine) as session:
        data = get_group(session, group_id)
    if data is None:
        return ServerMessage(message=f"The group with {group_id=} doesn't exists.")
    return data


###############################################################################
@social_groups.get(
    "/{group_id}/members",
    name="Get the members of a group.",
    response_model=list[UserPreview],
    responses={
        200: {"model": list[UserPreview], "description": "Members of a group."},
        403: {"model": ServerMessage, "description": "The given group doesn't exists."},

    },
)
def get_members(
    group_id: UUID,
    engine: Engine = Depends(get_engine),
):
    """Get the members of a group"""
    with Session(engine) as session:
        return get_members_by_group_id(session, group_id)


###############################################################################
class AddMember(BaseModel):
    member_to_add: UUID
    admin: bool


@social_groups.post(
    "/{group_id}/members",
    name="Add members to a group",
    # response_model=ServerMessage,
    # responses={
    #     200: {"model": ServerMessage, "description": "Succesfully added a new member"},
    #     404: {"model": ServerMessage, "description": "The given group doesn't exists."},
    # },
)
def post_add_member(
    group_id: UUID,
    body: AddMember,
    engine=Depends(get_engine),
    current_user: User = Depends(get_current_user),
):
    """Add member to a group."""
    with Session(engine) as session:
        if is_member(session, current_user.id, group_id):
            return JSONResponse(
                content={"detail": "Conflict"}, status_code=status.HTTP_409_CONFLICT
            )
        add_member(session, group_id, current_user.id, body.member_to_add)
        session.commit()
    return JSONResponse(content={"detail": ""})


###############################################################################
@social_groups.delete("/{group_id}/members/{member_id}", name="Remove member of a group")
def delete_member_from_group(
    group_id: UUID,
    member_id: UUID,
    engine=Depends(get_engine),
    current_user: User = Depends(get_current_user),
):
    """Removes a member from a group."""
    with Session(engine) as session:
        if not is_admin(session, current_user.id, group_id):
            return JSONResponse(
                {"detail": "Access Denied. You must be an admin of the group."},
                status.HTTP_403_FORBIDDEN,
            )
    remove_member(session, member_id, group_id)


###############################################################################
class PrivilegeChange(BaseModel):
    admin: bool  # should be true


@social_groups.patch("/{group_id}/members/{member_id}")
def patch_privilege(
    group_id: UUID,
    member_id: UUID,
    body: PrivilegeChange,
    engine=Depends(get_engine),
    current_user: User = Depends(get_current_user),
):
    """Upgrades the privileges of an member of a group."""
    with Session(engine) as session:
        if (
            is_admin(session, current_user.id, group_id)
            and current_user.id != member_id
        ):
            change_privilege(session, group_id, member_id, power=body.admin)
            return JSONResponse(None, status.HTTP_200_OK)


###############################################################################
# @social.post("/users")
# async def create_newuser_request(
#     new_user_email: str,
#     message_broker: Connection = Depends(get_mb),
#     engine: Engine = Depends(get_engine),
# ):
#     """Deliver a message to email_handler to make a new user"""

#     # If the email isn't valid then advice the user saying that we
#     # already have a account with this cadastred email.
#     if not is_email(new_user_email):
#         return JSONResponse(
#             {"detail": "Invalid email address."},
#             status_code=status.HTTP_400_BAD_REQUEST,
#         )
#     with Session(engine) as session:
#         if get_user(session, new_user_email):
#             return JSONResponse(
#                 {"detail": "Email already have a account cadastred here."},
#                 status_code=status.HTTP_409_CONFLICT,
#             )

#     binary_data = bytes(new_user_email, "UTF-8")
#     channel = await message_broker.channel()
#     await channel.basic_publish(binary_data, routing_key="new_user_request")
#     await channel.close()

#     return JSONResponse(
#         {
#             "detail": "Successfully created the new user request. Please verify your email."
#         },
#         status_code=status.HTTP_202_ACCEPTED,
#     )


###############################################################################
@social_users.get("")
def get_users(query: str | None = None, engine: Engine = Depends(get_engine)):
    with Session(engine) as session:
        return get_all_user_info(session, query=query)

@social_users.get("/me")
def get_me(
    user: User = Depends(get_current_user)
):
    return UserPreview.from_orm(user)

@social_users.post("")
def create_new_user(
    new_user: UserCreate,
    engine: Engine = Depends(get_engine),
):
    """"""
    if not is_email(new_user.email):
        return JSONResponse(
            {"detail": "Invalid mail address."}, status_code=status.HTTP_400_BAD_REQUEST
        )
    with Session(engine) as session:
        if get_user_by_email(session, new_user.email):
            return JSONResponse(
                {"detail": "Email already have a account cadastred here."},
                status_code=status.HTTP_409_CONFLICT,
            )
        create_user(session, new_user)


###############################################################################
@social_users.get("/{user_id}")
def get_user_profile_by_user_id(user_id: UUID, engine=Depends(get_engine)):
    """Returns some user data using the given id."""
    with Session(engine) as session:
        user = get_user_by_id(session, user_id)
        if user is not None:
            return UserPreview.from_orm(user)
        return JSONResponse(
            {"detail": f"Cannot return a user with the given {user_id=}"},
            status.HTTP_204_NO_CONTENT,
        )


###############################################################################
@social_users.get("/{user_id}/groups", response_model=list[Group])
def get_user_groups(user_id: UUID, engine=Depends(get_engine)):
    """Returns the groups from the given user"""
    with Session(engine) as session:
        user = get_user_by_id(session, user_id)
        if user is None:
            return JSONResponse(
                {"detail": f"User doesn't exists"}, status.HTTP_404_NOT_FOUND
            )
        groups = get_groups_by_user_id(session, user_id)
    return groups


###############################################################################
