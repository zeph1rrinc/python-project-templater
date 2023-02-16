import uvicorn

from .settings import settings


def main():
    uvicorn.run(
        'backend.app:app',
        host=settings.server_host,
        port=settings.server_port,
        reload=settings.debug,
    )


if __name__ == "__main__":
    main()
