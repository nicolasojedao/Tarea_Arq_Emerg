from fastapi import APIRouter, HTTPException, Header
from project.database import connection
from pydantic import BaseModel


class LocationCreate(BaseModel):
    company_id: int
    location_name: str
    location_country: str = None
    location_city: str = None
    location_meta: str = None



router = APIRouter()

@router.post("/", status_code=201)
def create_location(location: LocationCreate):
    try:
        connection.execute(
            """
            INSERT INTO location (id, company_id, location_name, location_country, location_city, location_meta)
            VALUES (nextval('seq_locationid'), ?, ?, ?, ?, ?)
            """,
            (location.company_id, location.location_name, location.location_country, location.location_city, location.location_meta),
        )
        return {"message": "Location created successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error creating location: {str(e)}")






@router.get("/")
def get_locations():
    try:
        result = connection.execute("SELECT * FROM location").fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error fetching locations: {str(e)}")







@router.delete("/{location_id}")
def delete_location(location_id: int):
    try:
        connection.execute("DELETE FROM location WHERE id = ?", (location_id,))
        return {"message": "Location deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error deleting location: {str(e)}")






@router.get("/{location_id}")
def get_location(location_id: int):
    try:
        result = connection.execute("SELECT * FROM location WHERE id = ?", (location_id,)).fetchone()
        if result:
            return result
        else:
            raise HTTPException(status_code=404, detail="Location not found")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error fetching location: {str(e)}")
