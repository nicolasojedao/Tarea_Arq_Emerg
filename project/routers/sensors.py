from fastapi import APIRouter, HTTPException, Header
from typing import List
from project.database import connection
import secrets
from pydantic import BaseModel

class SensorCreate (BaseModel):
    location_id: int
    sensor_name: str
    sensor_category: str = None
    sensor_meta: str = None


router = APIRouter()





@router.post("/", status_code=201)
def create_sensor(sensor: SensorCreate):
    sensor_api_key = secrets.token_hex(16)
    try:
        connection.execute(
            """
            INSERT INTO sensor (id, location_id, sensor_name, sensor_category, sensor_meta, sensor_api_key)
            VALUES (nextval('seq_sensorid'), ?, ?, ?, ?, ?)
            """,
            (sensor.location_id, sensor.sensor_name, sensor.sensor_category, sensor.sensor_meta, sensor_api_key),
        )
        return {"message": "Sensor created successfully", "sensor_api_key": sensor_api_key}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error creating sensor: {str(e)}")







@router.get("/")
def get_sensors():
    try:
        result = connection.execute("SELECT * FROM sensor").fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error fetching sensors: {str(e)}")







@router.delete("/{sensor_id}")
def delete_sensor(sensor_id: int):
    try:
        connection.execute("DELETE FROM sensor WHERE id = ?", (sensor_id,))
        return {"message": "Sensor deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error deleting sensor: {str(e)}")






@router.get("/{sensor_id}")
def get_sensor(sensor_id: int):
    try:
        result = connection.execute("SELECT * FROM sensor WHERE id = ?", (sensor_id,)).fetchone()
        if result:
            return result
        else:
            raise HTTPException(status_code=404, detail="Sensor not found")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error fetching sensor: {str(e)}")
