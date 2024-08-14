from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import auth, events, categories, purchases, payment, profiles, roles  # Asegúrate de que este 'payment' sea el de 'routers'
from database import engine, Base

# Importar los modelos para que se registren con la base de datos
from models import user, event, category, purchase, payment as payment_model

# Importar Celery (solo para que esté disponible, no iniciar desde aquí)
from celery_app import celery_app

app = FastAPI()

# Configurar los orígenes permitidos para CORS
origins = [
    "*",  # Agrega otros orígenes aquí según sea necesario
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Crear las tablas en la base de datos
Base.metadata.create_all(bind=engine)

# Incluir las rutas
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(profiles.router, prefix="/profiles", tags=["profiles"])
app.include_router(events.router, prefix="/events", tags=["events"])
app.include_router(categories.router, prefix="/categories", tags=["categories"])
app.include_router(purchases.router, prefix="/purchases", tags=["purchases"])
app.include_router(payment.router, prefix="/payments", tags=["payments"])
app.include_router(roles.router, prefix="/roles", tags=["Roles"])
