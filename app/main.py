from fastapi import FastAPI
from app.routes import auth_routes, report_routes, admin_routes
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Smart Waterborne Disease Early Warning System")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://waterborne-frontend.onrender.com","http://127.0.0.1:5500"],  # for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(auth_routes.router, prefix="/auth")
app.include_router(report_routes.router, prefix="/report")
app.include_router(admin_routes.router, prefix="/admin")  



