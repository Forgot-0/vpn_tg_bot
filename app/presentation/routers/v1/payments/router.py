from fastapi import APIRouter, status
from dishka.integrations.fastapi import DishkaRoute


router = APIRouter(route_class=DishkaRoute)



# @router.get(
#     "/",
#     status_code=status.HTTP_200_OK
# )
# async def get_list_payments(

# )