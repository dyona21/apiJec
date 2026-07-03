from pydantic_settings import BaseSettings
#esse cara aqui basicamente procura nas variaveis de ambiente se tem o 
# mesmo nome q está definido na classe abaixo para ele fazer o match
#COMEÇA O PROJETO POR AQUI

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "API JEC/Krona Futsal"
    
    # url para conectar com o banco postgresql://usuario:senha@servidor:porta/nome_do_banco
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/jec_krona"

    class Config:
        # permite criar um arquivo chamado .env na raiz do projeto que vai conter as senhas do seu projeto
        # para sobrescrever essas variáveis sem mexer no código
        env_file = ".env" 

#instanciando a classe 
settings = Settings()