from service.endpoints.add_movie_handler import api_router as movie_router
from service.endpoints.marks_handler import api_router as marks_router


list_of_routes = [
    movie_router,
    marks_router,
]

__all__ = ["list_of_routes"]
