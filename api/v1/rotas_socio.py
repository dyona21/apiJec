from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.database import get_db
from schemas.socio_schemas import SocioCreate, SocioResponse
from services import socio_service
from fastapi import APIRouter, Depends, HTTPException, status
from schemas.socio_schemas import AlterarPlanoSocio

router = APIRouter()

@router.post("/", response_model=SocioResponse, status_code=201)
def vincular_socio(socio: SocioCreate, db: Session = Depends(get_db)):
    """
    Vincula uma pessoa existente a um plano de sócio-torcedor.
    """
    return socio_service.criar_socio(db=db, socio_data=socio)

@router.delete("/{socio_id}", status_code=204)
def cancelar_plano_socio(socio_id: int, db: Session = Depends(get_db)):
    """
    Cancela o plano de um sócio (remove da tabela socio, mas mantém na tabela pessoa).
    """
    socio_service.deletar_socio(db=db, socio_id=socio_id)
    return None

@router.get("/{socio_id}", response_model=SocioResponse)
def buscar_dados_socio(socio_id: int, db: Session = Depends(get_db)):
    """
    Retorna os dados do plano de um sócio específico.
    """
    socio = socio_service.buscar_socio_por_id(db=db, socio_id=socio_id)
    
    if not socio:
        raise HTTPException(status_code=404, detail="Sócio não encontrado no sistema.")
        
    return socio

@router.patch("/{id_pessoa}/alterar-plano")
def alterar_plano_usuario(id_pessoa: int, dados: AlterarPlanoSocio, db: Session = Depends(get_db)):
    """
    Altera o plano de Sócio Torcedor de um usuário específico.
    """
    
    socio_atualizado = socio_service.atualizar_plano_do_socio(
        db=db, 
        id_pessoa=id_pessoa, 
        novo_id_plano=dados.id_plano
    )

    if not socio_atualizado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Registro de sócio não encontrado para esta pessoa."
        )

    return {
        "status": True,
        "mensagem": "Plano atualizado com sucesso!",
        "novo_id_plano": socio_atualizado.id_plano
    }