from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from core.config import settings

#cria a conexão com o DB usa a URL definida la no config
engine = create_engine(settings.DATABASE_URL)

#autocommit faz com q se uma operação foi interrompida por algum motivo n seja salvo nada no banco
#bind=engine é o que faz a conexão entre o banco de dados e a API
#autoflush = false só vai mandar os dados para o banco quando realmente for dado o sinal para ser enviado
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#é a classe mãe de todas as classes que vão expelhar as tabelas do banco de dados
Base = declarative_base()

#essa função aqui q entrega a conexão para as rotas que serão os outros arquivos, depois que uma rota termina de 
# pegar/colocar os dados ela fecha a sessão para n estourar o canal e nem estourar o banco com várias requisições simultaneas 
def get_db():
    db = SessionLocal()
    try:
        yield db  # disponibiliza a sessão para a rota usar
    finally:
        db.close()  #fecha a sessão depois de usada