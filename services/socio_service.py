from sqlalchemy.orm import Session
from fastapi import HTTPException
from models.socio import Socio
from models.pessoa import Pessoa
from models.plano_socio import PlanoSocio
from schemas.socio_schemas import SocioCreate

def criar_socio(db: Session, socio_data: SocioCreate):
    plano_existe = db.query(PlanoSocio).filter(PlanoSocio.id == socio_data.id_plano).first()
    if not plano_existe:
        raise HTTPException(status_code=404, detail="O plano escolhido não existe. A escolha de um plano válido é obrigatória.")

    pessoa_base = db.query(Pessoa).filter(Pessoa.id == socio_data.id_pessoa).first()
    if not pessoa_base:
        raise HTTPException(status_code=404, detail="Pessoa não encontrada. Cadastre os dados básicos antes de vincular ao plano de sócio.")

    socio_existente = db.query(Socio).filter(Socio.id_pessoa == socio_data.id_pessoa).first()
    if socio_existente:
        raise HTTPException(status_code=409, detail="Este usuário já possui um plano de sócio ativo.")

    novo_socio = Socio(
        id_pessoa=socio_data.id_pessoa,
        id_plano=socio_data.id_plano
    )
    
    db.add(novo_socio)
    db.commit()
    db.refresh(novo_socio)
    return novo_socio

def deletar_socio(db: Session, socio_id: int):
    """
    Remove o vínculo de sócio-torcedor de uma pessoa.
    O socio_id aqui é o próprio id_pessoa.
    """
    # 1. Busca o sócio pelo ID
    socio = db.query(Socio).filter(Socio.id_pessoa == socio_id).first()
    
    # 2. Se não existir, retorna erro 404
    if not socio:
        raise HTTPException(status_code=404, detail="Sócio não encontrado no sistema.")
        
    # 3. Deleta o registro apenas da tabela 'socio'
    db.delete(socio)
    db.commit()
    
    return {"mensagem": "Plano de sócio cancelado/excluído com sucesso."}


def buscar_socio_por_id(db: Session, socio_id: int):
    """
    Busca os dados de um sócio específico na tabela 'socio' usando o seu ID.
    """
    socio = db.query(Socio).filter(Socio.id_pessoa == socio_id).first()
    return socio

from sqlalchemy.orm import Session
from models.socio import Socio

def atualizar_plano_do_socio(db: Session, id_pessoa: int, novo_id_plano: int):
    # 1. Busca o registro atual onde o id_pessoa é igual ao que o Angular mandou
    socio_existente = db.query(Socio).filter(Socio.id_pessoa == id_pessoa).first()

    # 2. Se não achar, retorna None para a rota tratar
    if not socio_existente:
        return None

    # 3. A mágica acontece aqui! Trocamos o valor antigo pelo novo (Ex: do 3 para o 4)
    socio_existente.id_plano = novo_id_plano

    # 4. Salva a alteração no banco de dados
    db.commit()
    db.refresh(socio_existente)

    return socio_existente