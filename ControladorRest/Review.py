from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from Modelo.Review import Review
from Repositorio.Review import ReviewRepo
from Schema.Review import ReviewRead, ReviewCreate, ReviewUpdate
from ControladorRest import get_db


class ReviewRest:
    router = APIRouter(prefix="/reviews", tags=["Reviews"])

    @router.get("/", response_model=List[ReviewRead])
    def get_all_reviews(db: Session = Depends(get_db)):
        return db.query(Review).all()

    @router.get("/usuario/{usuario_id}", response_model=List[ReviewRead])
    def get_reviews_by_usuario(usuario_id: int, db: Session = Depends(get_db)):
        return ReviewRepo.fetch_by_usuario_id(db, usuario_id)

    @router.get("/producto/{producto_id}", response_model=List[ReviewRead])
    def get_reviews_by_producto(producto_id: int, db: Session = Depends(get_db)):
        return ReviewRepo.fetch_by_producto_id(db, producto_id)

    @router.get("/evento/{evento_id}", response_model=List[ReviewRead])
    def get_reviews_by_evento(evento_id: int, db: Session = Depends(get_db)):
        return ReviewRepo.fetch_by_evento_id(db, evento_id)

    @router.post("/", response_model=ReviewRead, status_code=status.HTTP_201_CREATED)
    def create_review(review: ReviewCreate, db: Session = Depends(get_db)):
        return ReviewRepo.create(db, review.dict())

    @router.put("/{review_id}", response_model=ReviewRead)
    def update_review(review_id: int, review: ReviewUpdate, db: Session = Depends(get_db)):
        updated = ReviewRepo.update(db, review_id, review.dict(exclude_unset=True))
        if not updated:
            raise HTTPException(status_code=404, detail="Review no encontrado")
        return updated

    @router.delete("/{review_id}/usuario/{usuario_id}", response_model=ReviewRead)
    def delete_review(review_id: int, usuario_id: int, db: Session = Depends(get_db)):
        deleted = ReviewRepo.delete(db, review_id, usuario_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="Review no encontrado o ya fue eliminado")
        return deleted
