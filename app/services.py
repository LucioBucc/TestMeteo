from sqlalchemy.orm import Session
from app.models import Site, MeteoInfo
from app.schemas import SiteCreate, MeteoInfoCreate
from datetime import date
import openmeteo_requests
import requests_cache
import pandas as pd
from retry_requests import retry
# Funzione per creare un nuovo record nella tabella Site


def create_site(db: Session, site: SiteCreate):
    db_meteo_info = create_meteo_info(db, site.lat, site.long )
    db_site = Site(long=site.long, lat=site.lat, id_meteo=db_meteo_info.id)
    db.add(db_site)
    db.commit()
    db.refresh(db_site)
    return db_site

# Funzione per creare un nuovo record nella tabella MeteoInfo


def create_meteo_info(db: Session, lat:float, long:float):
    meteo_info = get_info_meteo_api(lat, long)
    db_meteo_info = MeteoInfo(
        date=meteo_info[0],
        temperature_2m=meteo_info[1],
        relative_humidity_2m=meteo_info[2],
        dew_point_2m=meteo_info[3],
        pressure_msl=meteo_info[4],
        surface_pressure=meteo_info[5]
    )
    db.add(db_meteo_info)
    db.commit()
    db.refresh(db_meteo_info)
    return db_meteo_info

# Funzione per ottenere tutti i record della tabella Site


def get_sites(db: Session):
    return db.query(Site).all()

# Funzione per ottenere le informazioni meteo per un certo id


def get_meteo_info(db: Session, meteo_id: int):
    return db.query(MeteoInfo).filter(MeteoInfo.id == meteo_id).first()

# Funzione per ottenere i siti congiuntamente ai dati meteo


def get_sites_with_meteo_info(db: Session):
    return db.query(Site).join(MeteoInfo).all()

# Funziona che si interfaccia con l'api esterna

def get_info_meteo_api(lat:float, long:float):
    cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
    retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
    openmeteo = openmeteo_requests.Client(session=retry_session)

    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": long,
        "hourly": ["temperature_2m", "relative_humidity_2m", "dew_point_2m", "pressure_msl", "surface_pressure"]
    }
    responses = openmeteo.weather_api(url, params=params)

    response = responses[0]
    hourly = response.Hourly()
    hourly_temperature_2m = float(hourly.Variables(0).ValuesAsNumpy()[-1])
    hourly_relative_humidity_2m = float(
        hourly.Variables(1).ValuesAsNumpy()[-1])
    hourly_dew_point_2m = float(hourly.Variables(2).ValuesAsNumpy()[-1])
    hourly_pressure_msl = float(hourly.Variables(3).ValuesAsNumpy()[-1])
    hourly_surface_pressure = float(hourly.Variables(4).ValuesAsNumpy()[-1])

    hourly_data = {"date": pd.date_range(
        start=pd.to_datetime(hourly.Time(), unit="s", utc=True),
        end=pd.to_datetime(hourly.TimeEnd(), unit="s", utc=True),
        freq=pd.Timedelta(seconds=hourly.Interval()),
        inclusive="left"
    )}

    hourly_dataframe = pd.DataFrame(data=hourly_data)
    data = str(hourly_dataframe["date"].iloc[-1])
    res = (data,
           hourly_temperature_2m,
           hourly_relative_humidity_2m,
           hourly_dew_point_2m,
           hourly_pressure_msl,
           hourly_surface_pressure)
    return res
