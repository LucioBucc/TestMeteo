from fastapi import APIRouter, HTTPException, status, Depends,Request
from app import schemas
from sqlalchemy.orm import Session, joinedload
from app.middleware.db import get_db
from app import services
from app import models


router = APIRouter(prefix="/sites")


@router.get("/")
async def get_all_sites(db: Session = Depends(get_db)):
    sites = db.query(models.Site).options(joinedload(models.Site.meteo_info)).all()
    return sites

@router.get("/{site_id}")
async def get_site_by_id(site_id:int, db: Session = Depends(get_db)):
    site = db.query(models.Site).options(joinedload(models.Site.meteo_info)).filter(models.Site.id == site_id).first()
    if site is None:
        raise HTTPException(status_code=404, detail="Site not found")
    return site

@router.post("/")
async def create_new_site(site: schemas.SiteCreate, db: Session = Depends(get_db)):
    return services.create_site(db=db, site=site)