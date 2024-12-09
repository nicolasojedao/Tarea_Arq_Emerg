from fastapi import APIRouter, HTTPException, Header
from project.database import connection
from pydantic import BaseModel
import secrets

router = APIRouter()

class CompanyCreate(BaseModel):
    company_name: str


@router.post("/", status_code=201)
def create_company(company: CompanyCreate):
    company_api_key = secrets.token_hex(16)
    try:
        connection.execute(
            """
            INSERT INTO company (id, company_name, company_api_key)
            VALUES (nextval('seq_companyid'), ?, ?)
            """,
            (company.company_name, company_api_key),
        )
        return {"message": "Company created successfully", "company_api_key": company_api_key}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error creating company: {str(e)}")






@router.get("/")
def get_companies():
    try:
        result = connection.execute("SELECT * FROM company").fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error fetching companies: {str(e)}")






@router.delete("/{company_id}")
def delete_company(company_id: int):
    try:
        connection.execute("DELETE FROM company WHERE id = ?", (company_id,))
        return {"message": "Company deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error deleting company: {str(e)}")






@router.get("/{company_id}")
def get_company(company_id: int):
    try:
        result = connection.execute("SELECT * FROM company WHERE id = ?", (company_id,)).fetchone()
        if result:
            return result
        else:
            raise HTTPException(status_code=404, detail="Company not found")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error fetching company: {str(e)}")
