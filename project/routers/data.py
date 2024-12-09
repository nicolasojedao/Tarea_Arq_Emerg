from fastapi import APIRouter, HTTPException, Header, Query
from pydantic import BaseModel
from typing import List, Optional
from project.database import connection
import time
import json

router = APIRouter()


class SensorDataCreate(BaseModel):
    sensor_api_key: str
    json_data: List[dict]




@router.post("/", status_code=201)
def insert_sensor_data(sensor_data: SensorDataCreate):
    try:
        sensor = connection.execute(
            "SELECT id FROM sensor WHERE sensor_api_key = ?",
            (sensor_data.sensor_api_key,)
        ).fetchone()

        if not sensor:
            raise HTTPException(status_code=400, detail="Invalid sensor_api_key")

        sensor_id = sensor[0]
        current_timestamp = int(time.time())
        
        for data_entry in sensor_data.json_data:
            try:
                json_data_str = json.dumps(data_entry)
                connection.execute(
                    """
                    INSERT INTO sensor_data (id, sensor_id, timestamp, data)
                    VALUES (nextval('seq_sensor_dataid'), ?, ?, ?)
                    """,
                    (sensor_id, current_timestamp, json_data_str),
                )
            except Exception as e:
                raise HTTPException(status_code=400, detail=f"Error parsing JSON data: {str(e)}")


        return {"message": "Data inserted successfully"}

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error inserting sensor data: {str(e)}")

@router.get("/")
def get_sensor_data(
    company_api_key: str = Header(...),
    from_timestamp: int = Query(..., alias="from"),
    to_timestamp: int = Query(..., alias="to"),
    sensor_ids: List[int] = Query(...)
):
    try:
        company = connection.execute(
            "SELECT id FROM company WHERE company_api_key = ?",
            (company_api_key,)
        ).fetchone()

        if not company:
            raise HTTPException(status_code=400, detail="Invalid company_api_key")

        company_id = company[0]

        valid_sensors = connection.execute(
            """
            SELECT sensor.id FROM sensor
            JOIN location ON sensor.location_id = location.id
            WHERE location.company_id = ?
            """,
            (company_id,)
        ).fetchall()

        valid_sensor_ids = {sensor[0] for sensor in valid_sensors}
        if not all(sensor_id in valid_sensor_ids for sensor_id in sensor_ids):
            raise HTTPException(status_code=400, detail="Invalid sensor_id(s) for this company")

        query = """
        SELECT * FROM sensor_data
        WHERE sensor_id IN (%s)
        AND timestamp BETWEEN ? AND ?
        """ % (",".join(["?"] * len(sensor_ids)))

        result = connection.execute(query, (*sensor_ids, from_timestamp, to_timestamp)).fetchall()

        return result

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error fetching sensor data: {str(e)}")
