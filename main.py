from typing import Union
from fastapi import FastAPI, Request
from pydantic import BaseModel, EmailStr
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import uvicorn

# Inicialitzem l'aplicació FastAPI
app = FastAPI()

# Array global d'usuaris
usuaris = []

# Configurem el directori de plantilles (templates)
templates = Jinja2Templates(directory="templates")

# Model Pydantic per validar les dades d'un usuari
class Usuari(BaseModel):
    Nom: str
    Cognom: str
    Edat: int
    email: EmailStr

# PUT: Actualitzar un usuari existent
@app.put("/usuaris/{usuari_id}")
def update_usuari(usuari_id: int, usuari: Usuari):
    if usuari_id >= len(usuaris):
        return {"error": "Usuari no trobat"}
    usuaris[usuari_id] = usuari
    return {"message": f"Usuari {usuari.Nom} {usuari.Cognom} actualitzat correctament"}

# POST: Crear un nou usuari
@app.post("/usuaris/")
def crear_usuari(usuari: Usuari):
    usuaris.append(usuari)
    return {"missatge": f"Usuari {usuari.Nom} {usuari.Cognom} afegit correctament"}

# GET: Llistat usuaris
@app.get("/usuaris/", response_class=HTMLResponse)
def llegir_usuaris(request: Request):
    return templates.TemplateResponse("usuari.html", {"request": request, "usuaris": usuaris})

# GET: Mostrar els detalls d'un usuari
@app.get("/usuaris/{usuari_id}", response_class=HTMLResponse)
def read_user(usuari_id: int, request: Request):
    if usuari_id >= len(usuaris):
        return {"error": "Usuari no trobat"}
    return templates.TemplateResponse("detall_usuari.html", {"request": request, "usuari": usuaris[usuari_id]})

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)
