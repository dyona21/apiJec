from sqlalchemy.orm import Session
from fastapi import HTTPException
from models.pessoa import Pessoa
from schemas.pessoa_schema import PessoaCreate
from models.socio import Socio         
from models.plano_socio import PlanoSocio

def criar_pessoa_jogador(db: Session, pessoa_data: PessoaCreate):
    # 1. Converte os dados do Schema (Pydantic) para o Model (SQLAlchemy)
    nova_pessoa = Pessoa(
        nome=pessoa_data.nome,
        cpf=pessoa_data.cpf,
        email=pessoa_data.email,
        senha=pessoa_data.senha, 
        data_nascimento=pessoa_data.data_nascimento,
        adm=pessoa_data.adm
    )
    
    # 2. Adiciona a nova pessoa na sessão (preparando para salvar)
    db.add(nova_pessoa)
    
    # 3. Confirma a gravação no banco de dados
    # Lembra do nosso "autocommit=False" no database.py? É aqui que apertamos o botão de salvar!
    db.commit()
    
    # 4. Atualiza o objeto no Python com os dados gerados pelo PostgreSQL (como o ID)
    db.refresh(nova_pessoa)
    
    # 5. Retorna a pessoa cadastrada (que depois será enviada para o Angular)
    return nova_pessoa

def buscar_pessoa_por_id(db: Session, pessoa_id: int):
    # Faz um SELECT * FROM pessoa WHERE id = pessoa_id
    # O .first() pega o primeiro resultado (ou devolve None se não achar)
    return db.query(Pessoa).filter(Pessoa.id == pessoa_id).first()

def listar_pessoas(db: Session, skip: int = 0, limit: int = 100):
    # Faz um SELECT * FROM pessoa LIMIT 100 OFFSET 0
    # Ótimo para fazer paginação no front-end depois
    return db.query(Pessoa).offset(skip).limit(limit).all()

def atualizar_pessoa(db: Session, pessoa_id: int, dados_atualizados: dict):
    # 1. Busca a pessoa existente
    pessoa = buscar_pessoa_por_id(db, pessoa_id)
    if not pessoa:
        raise HTTPException(status_code=404, detail="Pessoa não encontrada.")
    
    # 2. Atualiza apenas os campos que foram enviados
    for chave, valor in dados_atualizados.items():
        setattr(pessoa, chave, valor)
        
    db.commit()
    db.refresh(pessoa)
    return pessoa

def deletar_pessoa(db: Session, pessoa_id: int):
    pessoa = buscar_pessoa_por_id(db, pessoa_id)
    if not pessoa:
        raise HTTPException(status_code=404, detail="Pessoa não encontrada.")
        
    db.delete(pessoa)
    db.commit()
    return {"mensagem": "Registro apagado com sucesso!"}

def criar_pessoa(db: Session, pessoa_data: PessoaCreate):
    # 1. Cria a pessoa base
    nova_pessoa = Pessoa(
        nome=pessoa_data.nome,
        cpf=pessoa_data.cpf,
        email=pessoa_data.email,
        senha=pessoa_data.senha, 
        data_nascimento=pessoa_data.data_nascimento,
        adm=pessoa_data.adm
    )
    
    db.add(nova_pessoa)
    
    # 2. O FLUSH: Gera o ID no banco, mas ainda permite cancelar a operação se der erro abaixo
    db.flush() 

    # 3. Se o Angular mandou um id_plano, criamos o Sócio na mesma transação!
    if pessoa_data.id_plano:
        # Validação de segurança: verifica se o plano existe
        plano_existe = db.query(PlanoSocio).filter(PlanoSocio.id == pessoa_data.id_plano).first()
        if not plano_existe:
            db.rollback() # Cancela a criação da Pessoa
            raise HTTPException(status_code=404, detail="O plano escolhido não existe.")
            
        novo_socio = Socio(
            id_pessoa=nova_pessoa.id, # Pega o ID gerado pelo flush ali em cima
            id_plano=pessoa_data.id_plano
        )
        db.add(novo_socio)
    
    # 4. Salva TUDO de uma vez só no banco (Pessoa + Sócio)
    db.commit()
    db.refresh(nova_pessoa)
    
    return nova_pessoa