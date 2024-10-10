from ninja import NinjaAPI
from backendApi.utils.backend_auth import SupabaseTokenAuthentication
from user.api import router as users_router
from backendApi.api import router as backend_router
from genres.api import router as genres_router
from games.api import router as games_router
from platforms.api import router as platforms_router
from requirements.api import router as requirements_router

api = NinjaAPI() # no auth
#api = NinjaAPI(auth=SupabaseTokenAuthentication()) # global auth

# api routers
api.add_router("/", backend_router)
api.add_router("/users/", users_router)
api.add_router("/genres/", genres_router)
api.add_router("/games/", games_router)
api.add_router("/platforms/", platforms_router)
api.add_router("/requirements/", requirements_router)