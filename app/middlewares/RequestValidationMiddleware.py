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

    # Prepare CORS headers to be returned in responses (as requested)
    cors_headers = {
        "Access-Control-Allow-Headers": "Origin,X-Requested-With,Content-Type,Accept,Authorization",
        "Access-Control-Allow-Methods": "GET,POST,PUT,DELETE,OPTIONS,PATCH",
        "Access-Control-Allow-Origin": CLIENT_URL,
    }

    if request.method == "OPTIONS":
        # Immediate response for preflight with the required CORS headers
        return JSONResponse(content={}, status_code=200, headers=cors_headers)

    # Check request origin (manual CORS validation)
    origin = request.headers.get("origin", "")
    if origin and origin not in [CLIENT_URL, API_URL_HTTP, API_URL_HTTPS]:
        return JSONResponse(
            content={"Title": "Forbidden", "StatusCode": 403},
            status_code=403,
            headers=cors_headers
        )

    # Validate JWT token
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        return JSONResponse(
            content={"Title": "Unauthorized", "StatusCode": 401},
            status_code=401,
            headers=cors_headers
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
            status_code=401,
            headers=cors_headers
        )
    except JWTError:
        # Invalid or tampered token
        return JSONResponse(
            content={"Title": "Unauthorized", "StatusCode": 401},
            status_code=401,
            headers=cors_headers
        )
    except Exception:
        # Any other unexpected validation error
        return JSONResponse(
            content={"Title": "Unauthorized", "StatusCode": 401},
            status_code=401,
            headers=cors_headers
        )

    # If everything is fine, continue to the next middleware or route
    # Call next and attach the CORS headers to the response so clients receive them
    response = await call_next(request)
    # Merge CORS headers into response headers (don't overwrite existing headers unintentionally)
    for k, v in cors_headers.items():
        # only set if not already present
        if k not in response.headers:
            response.headers[k] = v

    return response
