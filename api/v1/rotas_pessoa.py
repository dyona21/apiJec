from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.database import get_db
from models.plano_socio import PlanoSocio
from schemas.pessoa_schema import PessoaCreate, PessoaResponse
from services import pessoa_service
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from models.pessoa import Pessoa
from models.atleta import Atleta
from models.socio import Socio
from schemas.socio_schemas import LoginSocio

router = APIRouter()

@router.post("/", response_model=PessoaResponse, status_code=201)
def criar_nova_pessoa(pessoa: PessoaCreate, db: Session = Depends(get_db)):
    """
    Cadastra um novo usuário base (Pessoa) no sistema.
    """
    return pessoa_service.criar_pessoa(db=db, pessoa_data=pessoa)

@router.post("/jogador", response_model=PessoaResponse, status_code=201)
def criar_nova_pessoa(pessoa: PessoaCreate, db: Session = Depends(get_db)):
    """
    Cadastra um novo usuário base (Pessoa) no sistema.
    """
    return pessoa_service.criar_pessoa_jogador(db=db, pessoa_data=pessoa)

@router.get("/", response_model=List[PessoaResponse])
def listar_todas_pessoas(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return pessoa_service.listar_pessoas(db=db, skip=skip, limit=limit)

@router.get("/{pessoa_id}", response_model=PessoaResponse)
def buscar_pessoa(pessoa_id: int, db: Session = Depends(get_db)):
    pessoa = pessoa_service.buscar_pessoa_por_id(db=db, pessoa_id=pessoa_id)
    if not pessoa:
        raise HTTPException(status_code=404, detail="Pessoa não encontrada.")
    return pessoa

@router.put("/{pessoa_id}", response_model=PessoaResponse)
def atualizar_dados_pessoa(pessoa_id: int, pessoa_atualizada: PessoaCreate, db: Session = Depends(get_db)):
    dados = pessoa_atualizada.model_dump(exclude_unset=True)
    return pessoa_service.atualizar_pessoa(db=db, pessoa_id=pessoa_id, dados_atualizados=dados)

@router.delete("/{pessoa_id}", status_code=204)
def deletar_cadastro_pessoa(pessoa_id: int, db: Session = Depends(get_db)):
    pessoa_service.deletar_pessoa(db=db, pessoa_id=pessoa_id)
    return None



@router.post("/login")
def validar_login(dados_login: LoginSocio, db: Session = Depends(get_db)):
    
    pessoa_encontrada = db.query(Pessoa).filter(Pessoa.cpf == dados_login.cpf).first()

    if not pessoa_encontrada or pessoa_encontrada.senha != dados_login.senha:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="CPF ou senha incorretos." 
        )

    socio_encontrado = db.query(Socio).filter(Socio.id_pessoa == pessoa_encontrada.id).first()

    if not socio_encontrado:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Este usuário ainda não possui um plano de Sócio Torcedor ativo."
        )
    plano_do_banco: PlanoSocio = socio_encontrado.plano

    return {
        "status": True,
        "pessoa": {
            "id": pessoa_encontrada.id,
            "email": pessoa_encontrada.email,
            "aniversario": pessoa_encontrada.data_nascimento,
            "adm": pessoa_encontrada.adm,
            "nome": pessoa_encontrada.nome, 
            "cpf": pessoa_encontrada.cpf,
            "plano": {
                "nome_plano": plano_do_banco.nome_plano,
                "valor": plano_do_banco.valor,
                "beneficios": plano_do_banco.beneficio,
                "vantagens": plano_do_banco.vantagens,
                "forma_pagamento": plano_do_banco.forma_pagamento
            },
            "idPlano": socio_encontrado.id_plano, 
            "atleta": pessoa_encontrada.atleta
        }
    }