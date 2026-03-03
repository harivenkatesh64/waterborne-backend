from pydantic import BaseModel

class HealthReport(BaseModel):
    village: str
    diarrhea_cases: int
    fever_cases: int
    vomiting_cases: int
    jaundice_cases: int
    risk_factors: str
    water_source_condition: str