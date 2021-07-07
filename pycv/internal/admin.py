from fastapi import Depends, APIRouter
from dependencies import get_token_header

router = APIRouter(
    prefix="/admin",
    tags=["admin"],
    dependencies=[Depends(get_token_header)],
    responses={418: {"description": "I'm a teapot"}},
)


@router.get("/", tags=["admin"])
async def read_users():
    return {"message": "Hello Admin!"}
