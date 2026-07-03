from sqlalchemy.orm import Session
from models.plano_socio import PlanoSocio
from schemas.planoSocio_schema import PlanoSocioCreate

def criar_plano(db: Session, plano_data: PlanoSocioCreate):
    """
    Cadastra um novo plano de sócio-torcedor no banco de dados.
    """
    novo_plano = PlanoSocio(
        nome_plano=plano_data.nome_plano,
        valor=plano_data.valor,
        beneficios=plano_data.beneficios
    )
    
    db.add(novo_plano)
    db.commit()
    db.refresh(novo_plano)
    
    return novo_plano

def listar_planos(db: Session):
    """
    Retorna todos os planos disponíveis.
    """
    return db.query(PlanoSocio).all()

def buscar_plano_por_id(db: Session, plano_id: int):
    return db.query(PlanoSocio).filter(PlanoSocio.id == plano_id).first()