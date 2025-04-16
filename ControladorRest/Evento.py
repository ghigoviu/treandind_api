from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from Modelo.EventoAsistente import EventoAsistente
from Repositorio.Evento import EventoRepo
from Schema.Evento import EventoCreate, EventoRead, EventoUpdate, EventoAsistenteRead
from ControladorRest import get_db

from Schema.Evento import EventoConAsistentes
from Schema.EventoAsistente import EventoAsistenteCreate


class EventoRest:
    router = APIRouter(prefix="/eventos", tags=["Eventos"])

    @router.post("/", response_model=EventoRead, status_code=status.HTTP_201_CREATED)
    def crear(evento: EventoCreate, db: Session = Depends(get_db)):
        return EventoRepo.create(db, evento.dict())

    @router.post("/{evento_id}/registrar-asistente", response_model=EventoAsistenteRead)
    def registrar_asistente(evento_id: int, body: EventoAsistenteCreate, db: Session = Depends(get_db)):
        # Opcional: Validar que no esté ya registrado
        existente = db.query(EventoAsistente).filter_by(evento_id=evento_id, usuario_id=body.usuario_id).first()
        if existente:
            raise HTTPException(status_code=400, detail="El usuario ya está registrado en este evento.")

        return EventoRepo.registrar_asistente(db, evento_id, body.usuario_id)

    @router.get("/", response_model=List[EventoRead])
    def get_all(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
        return EventoRepo.fetch_all(db, skip, limit)

    @router.get("/{evento_id}", response_model=EventoRead)
    def get_by_id(evento_id: int, db: Session = Depends(get_db)):
        evento = EventoRepo.fetch_by_id(db, evento_id)
        if not evento:
            raise HTTPException(status_code=404, detail="Evento no encontrado.")
        return evento

    @router.get("/{evento_id}/detalle", response_model=EventoConAsistentes)
    def get_con_asistentes(evento_id: int, db: Session = Depends(get_db)):
        evento = EventoRepo.fetch_con_asistentes(db, evento_id)
        if not evento:
            raise HTTPException(status_code=404, detail="Evento no encontrado.")

        return {
            **EventoRead.from_orm(evento).dict(),
            "asistentes": evento.asistentes,
            "total_asistentes": len(evento.asistentes)
        }

    @router.put("/{evento_id}", response_model=EventoRead)
    def actualizar(evento_id: int, evento: EventoUpdate, db: Session = Depends(get_db)):
        actualizado = EventoRepo.update(db, evento_id, evento.dict(exclude_unset=True))
        if not actualizado:
            raise HTTPException(status_code=404, detail="Evento no encontrado.")
        return actualizado

    @router.delete("/{evento_id}", response_model=EventoRead)
    def eliminar(evento_id: int, db: Session = Depends(get_db)):
        eliminado = EventoRepo.delete(db, evento_id)
        if not eliminado:
            raise HTTPException(status_code=404, detail="Evento no encontrado.")
        return eliminado
