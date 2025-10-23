from fastapi import Request
from fastapi.responses import JSONResponse
from jose import jwt, JWTError, ExpiredSignatureError
import os

# Environment variables and default values
CLIENT_URL = os.getenv("CLIENT_URL", "http://localhost:5173")
API_URL_HTTP = "http://localhost:8000"
API_URL_HTTPS = "https://localhost:8000"
JWT_SECRET = os.getenv("AUTH_API_JWT_SECRET", "secret")

async def request_validation_middleware(request: Request, call_next):
    path = request.url.path

    # Allow public routes (Swagger, OpenAPI, or index.html)
    if path.startswith("/docs") or path.startswith("/openapi") or path.startswith("/index.html"):
        return await call_next(request)

    # Allow preflight requests (CORS OPTIONS)
    if request.method == "OPTIONS":
        return await call_next(request)

    # Check request origin (manual CORS validation)
    origin = request.headers.get("origin", "")
    if origin and origin not in [CLIENT_URL, API_URL_HTTP, API_URL_HTTPS]:
        return JSONResponse(
            content={"Title": "Forbidden", "StatusCode": 403},
            status_code=403
        )

    # Validate JWT token
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        return JSONResponse(
            content={"Title": "Unauthorized", "StatusCode": 401},
            status_code=401
        )

    # Extract the Bearer token
    token = auth_header.replace("Bearer ", "").strip()

    try:
        # Decode and validate the JWT token
        jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
    except ExpiredSignatureError:
        # Token expired
        return JSONResponse(
            content={"Title": "Unauthorized", "StatusCode": 401},
            status_code=401
        )
    except JWTError:
        # Invalid or tampered token
        return JSONResponse(
            content={"Title": "Unauthorized", "StatusCode": 401},
            status_code=401
        )
    except Exception:
        # Any other unexpected validation error
        return JSONResponse(
            content={"Title": "Unauthorized", "StatusCode": 401},
            status_code=401
        )

    # If everything is fine, continue to the next middleware or route
    response = await call_next(request)
    return response
