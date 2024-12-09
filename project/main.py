from fastapi import FastAPI
from project.database import initialize_database
from project.routers import sensors, locations, data, company




app = FastAPI()

initialize_database()

app.include_router(sensors.router, prefix="/api/v1/sensors", tags=["Sensors"])
app.include_router(locations.router, prefix="/api/v1/locations", tags=["Locations"])
app.include_router(data.router, prefix="/api/v1/sensor_data", tags=["Sensor Data"])
app.include_router(company.router, prefix="/api/v1/companies", tags=["Companies"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the IoT API"}
