from pydantic import BaseModel
from datetime import date


# Schema per creare un nuovo sito
class SiteBase(BaseModel):
    long: float
    lat: float
    id_meteo: int

class SiteCreate(BaseModel):
    long: float
    lat: float
# Schema per creare un nuovo record meteo
class MeteoInfoBase(BaseModel):
    date: date
    temperature_2m: float
    relative_humidity_2m: float
    dew_point_2m: float
    pressure_msl: float
    surface_pressure: float

class MeteoInfoCreate(MeteoInfoBase):
    pass

