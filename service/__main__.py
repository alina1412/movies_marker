from fastapi import FastAPI
from uvicorn import run

from service.config import get_settings
from service.endpoints import list_of_routes


def get_app() -> FastAPI:
    application = FastAPI(
        title="Backend",
        description="",
        docs_url="/docs",
        openapi_url="/openapi.json",
        version="1.0.0",
    )

    settings = get_settings()

    for route in list_of_routes:
        application.include_router(route, prefix=settings.API_PREFIX)

    application.state.settings = settings
    return application


app = get_app()


if __name__ == "__main__":
    app_settings = get_settings()
    run(
        "service.__main__:app",
        host=app_settings.APP_HOST,
        port=app_settings.APP_PORT,
        reload=True,
        reload_dirs=["service", "tests"],
        log_level=app_settings.LOG_LEVEL,
    )
