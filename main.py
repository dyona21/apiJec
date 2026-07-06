from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.config import settings
from api.v1 import rotas_pessoa, rotas_atleta, rotas_partida, rotas_socio, rotas_competicao, rotas_plano_socio

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="API para gerenciamento do site oficial do JEC/Krona Futsal",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"], 
)

app.include_router(rotas_pessoa.router, prefix=f"{settings.API_V1_STR}/pessoas", tags=["Pessoas"])
app.include_router(rotas_atleta.router, prefix=f"{settings.API_V1_STR}/atletas", tags=["Elenco"])
app.include_router(rotas_partida.router, prefix=f"{settings.API_V1_STR}/partidas", tags=["Calendário de Jogos"])
app.include_router(rotas_socio.router, prefix=f"{settings.API_V1_STR}/socios", tags=["Sócios-Torcedores"])
app.include_router(rotas_competicao.router, prefix=f"{settings.API_V1_STR}/competicoes", tags=["Sala de Troféus"])
app.include_router(rotas_plano_socio.router, prefix=f"{settings.API_V1_STR}/planos", tags=["Planos de Sócio"])

@app.get("/", tags=["Health Check"])
async def root():
    return {
        "status": "Online",
        "message": "API do JEC rodando com sucesso!"
    }