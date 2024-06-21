from fastapi import FastAPI
from fastapi.responses import JSONResponse
from users.routes import router as user_list_router, user_router
from auth.route import router as auth_router
from account.routes import router as account_router
from core.security import JWTAuth
from starlette.middleware.authentication import AuthenticationMiddleware


app = FastAPI()

app.include_router(user_router)
app.include_router(auth_router)
app.include_router(user_list_router)

app.include_router(account_router)


# Add Middleware
app.add_middleware(AuthenticationMiddleware, backend=JWTAuth())

@app.get('/')
def health_check():
    return JSONResponse(content={"status": "Running!"})