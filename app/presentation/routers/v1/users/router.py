from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter



router = APIRouter(route_class=DishkaRoute)

