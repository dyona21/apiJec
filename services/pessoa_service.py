from sqlalchemy.orm import Session
from fastapi import HTTPException
from models.pessoa import Pessoa
from schemas.pessoa_schema import PessoaCreate
from models.socio import Socio         
from models.plano_socio import PlanoSocio

def criar_pessoa_jogador(db: Session, pessoa_data: PessoaCreate):
    nova_pessoa = Pessoa(
        nome=pessoa_data.nome,
        cpf=pessoa_data.cpf,
        email=pessoa_data.email,
        senha=pessoa_data.senha, 
        data_nascimento=pessoa_data.data_nascimento,
        adm=pessoa_data.adm
    )
    
    db.add(nova_pessoa)
    
    db.commit()
    
    db.refresh(nova_pessoa)
    
    return nova_pessoa

def buscar_pessoa_por_id(db: Session, pessoa_id: int):
    return db.query(Pessoa).filter(Pessoa.id == pessoa_id).first()

def listar_pessoas(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Pessoa).offset(skip).limit(limit).all()

def atualizar_pessoa(db: Session, pessoa_id: int, dados_atualizados: dict):
    pessoa = buscar_pessoa_por_id(db, pessoa_id)
    if not pessoa:
        raise HTTPException(status_code=404, detail="Pessoa não encontrada.")
    
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
    nova_pessoa = Pessoa(
        nome=pessoa_data.nome,
        cpf=pessoa_data.cpf,
        email=pessoa_data.email,
        senha=pessoa_data.senha, 
        data_nascimento=pessoa_data.data_nascimento,
        adm=pessoa_data.adm
    )
    
    db.add(nova_pessoa)
    
    db.flush() 

    if pessoa_data.id_plano:
        plano_existe = db.query(PlanoSocio).filter(PlanoSocio.id == pessoa_data.id_plano).first()
        if not plano_existe:
            db.rollback() 
            raise HTTPException(status_code=404, detail="O plano escolhido não existe.")
            
        novo_socio = Socio(
            id_pessoa=nova_pessoa.id, 
            id_plano=pessoa_data.id_plano
        )
        db.add(novo_socio)
    
    db.commit()
    db.refresh(nova_pessoa)
    
    return nova_pessoa