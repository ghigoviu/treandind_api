from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from Repositorio.Highlight import HighlightRepo
from Schema.Highlight import HighlightCreate, HighlightRead
from ControladorRest import get_db


class HighlightRest:
    router = APIRouter(prefix="/highlights", tags=["Highlights"])

    @router.get("/", response_model=List[HighlightRead])
    def get_all(db: Session = Depends(get_db)):
        return HighlightRepo.fetch_all(db)

    @router.get("/{highlight_id}", response_model=HighlightRead)
    def get_by_id(highlight_id: int, db: Session = Depends(get_db)):
        highlight = HighlightRepo.fetch_by_id(db, highlight_id)
        if not highlight:
            raise HTTPException(status_code=404, detail="Highlight no encontrado")
        return highlight

    @router.post("/", response_model=HighlightRead)
    def create(highlight: HighlightCreate, db: Session = Depends(get_db)):
        return HighlightRepo.create(db, highlight.dict())

    @router.put("/{highlight_id}", response_model=HighlightRead)
    def update(highlight_id: int, highlight: HighlightCreate, db: Session = Depends(get_db)):
        updated = HighlightRepo.update(db, highlight_id, highlight.dict())
        if not updated:
            raise HTTPException(status_code=404, detail="Highlight no encontrado")
        return updated

    @router.delete("/{highlight_id}", response_model=HighlightRead)
    def delete(highlight_id: int, db: Session = Depends(get_db)):
        deleted = HighlightRepo.delete(db, highlight_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="Highlight no encontrado")
        return deleted
