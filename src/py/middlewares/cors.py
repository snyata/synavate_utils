from fastapi.middleware.cors import CORSMiddleware

origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:3001",
    "https://timelesslove.ai",
    "https://www.timelesslove.ai",
    "http://timelesslove.ai",
    "http://www.timelesslove.ai",
    "https://chat.timelesslove.ai",
    "*",
]


def add_cors_middleware(app):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )