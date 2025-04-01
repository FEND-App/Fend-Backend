from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import models
from models.news import News

from schemas.news import NewsUpdate

app = FastAPI()
router = APIRouter()

models.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get('/News/')
async def get_news(db: Session = Depends(get_db)):
    try:
        news = db.query(models.News).all()
        return news
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error interno del sistema: {str(e)}")


@router.get('/News/{id_news}')
async def get_news_by_id(id_news: int, db: Session = Depends(get_db)):
    try:
        news = db.query(models.News).filter(
            models.News.id_news == id_news).first()

        if not news:
            raise HTTPException(status_code=404, detail="Noticia no encontrada")

        return news
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error interno del sistema: {str(e)}")


@router.put('/News/{id_news}')
async def update_news(id_news: int, data: NewsUpdate, db: Session = Depends(get_db)):
    try:
        news = db.query(models.News).filter(
            models.News.id_news == id_news).first()

        if not news:
            raise HTTPException(status_code=404, detail="Noticia no encontrada")

        if data.content:
            news.content = data.content
        if data.expiration_date:
            news.expiration_date = data.expiration_date
        if data.residental_management:
            news.residental_management = data.residental_management
        if data.status is not None:
            news.status = data.status

        db.commit()
        db.refresh(news)

        return {"message": "Noticia actualizada con exito"}
    except HTTPException as e:
        raise e
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500, detail=f"Error interno del sistema: {str(e)}")

@router.delete('/News/{id_news}')
async def delete_news(id_news: int, db: Session = Depends(get_db)):
    try:
        news = db.query(models.News).filter(
            models.News.id_news == id_news).first()

        if not news:
            raise HTTPException(status_code=404, detail="Noticia no encontrada")

        db.delete(news)
        db.commit()

        return {"message": "Noticia eliminada con exito"}
    except HTTPException as e:
        raise e
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500, detail=f"Error interno del sistema: {str(e)}")