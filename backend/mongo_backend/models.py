from beanie import Document, Link, PydanticObjectId
from pydantic import BaseModel, Field
from typing import Optional, Literal
from datetime import datetime
from pymongo import IndexModel
from pathlib import Path


class Compound(Document):
    compound_id: str = Field(...)
    SMILES: str = Field(...)
    Solvent_Type: Literal["Solvent", "Salt"] = Field(...)
    Molar_Mass: float = Field(...)
    Chem_Formula: Optional[str] = None
    Density: Optional[float] = None

    class Settings:
        name = "compound"
        indexes = [
            IndexModel([("compound_id", 1)], unique=True)       
        ]

class CompoundIDProjection(BaseModel):
    compound_id: str = Field(...)        

class CompoundEntry(BaseModel):
    compound: Link[Compound]
    compound_id: str
    quantity: float
    quantity_type: Literal["weight_percent", "volume_percent", "moles"]  

class PreparationFormulation(Document):
    description: str
    formulation: list[CompoundEntry]
    created_at: datetime = Field(default_factory=datetime.now)


    class Settings:
        name = "preparationFormulation"
        indexes = [
            IndexModel([("description", 1)], unique=False)        
        ]

class InputCompoundEntry(BaseModel):
    compound_id: str
    quantity: float
    quantity_type: Literal["weight_percent", "volume_percent", "moles"]  

class InputFormulation(BaseModel):
    description: str
    formulation: list[InputCompoundEntry]
    CE: Optional[float] = Field(default=None, ge = 0, le = 100.0)
    LCE: Optional[float] = Field(default=None, ge = 0)
    cycle: Optional[int] = Field(default=None, ge = 0)
    current: Optional[float] = Field(default=None, ge = 0)
    capacity: Optional[float] = Field(default=None, ge = 0)
    
class ElementRatio(BaseModel):
    FC: float = Field(..., ge=0)
    OC: float = Field(..., ge=0)
    FO: float = Field(..., ge=0)
    InOr: float = Field(..., ge=0)
    F: float = Field(..., ge=0)
    sF: float = Field(..., ge=0)
    aF: float = Field(..., ge=0)
    O: float = Field(..., ge=0)
    sO: float = Field(..., ge=0)
    aO: float = Field(..., ge=0) 
    C: float = Field(..., ge=0)
    sC: float = Field(..., ge=0)
    aC: float = Field(..., ge=0)


class PreparationFormulationList(BaseModel):
    formulations: list[PreparationFormulation]

class PreparationFormulationListPagination(PreparationFormulationList):
    page: int = Field(ge=1, default=1)
    has_more: bool    

class UpdateFormulation(BaseModel):
    description: Optional[str] = None
    formulation: Optional[list[InputCompoundEntry]] = None 
    CE: Optional[float] = Field(default=None, ge = 0, le = 100.0)
    LCE: Optional[float] = Field(default=None, ge = 0)
    cycle: Optional[int] = Field(default=None, ge = 0)
    current: Optional[float] = Field(default=None, ge = 0)
    capacity: Optional[float] = Field(default=None, ge = 0)     


class MLFormulation(Document):
    preparation_id: Link[PreparationFormulation]
    description: str
    formulation: list[CompoundEntry]
    element_ratio: ElementRatio
    CE: Optional[float] = Field(default=None, ge = 0, le = 100.0)
    LCE: Optional[float] = Field(default=None, ge = 0)
    cycle: Optional[int] = Field(default=None, ge = 0)
    current: Optional[float] = Field(default=None, ge = 0)
    capacity: Optional[float] = Field(default=None, ge = 0)

    class Settings:
        name = "MLFormulation"
        indexes = [
            IndexModel([("preparation_id", 1)], unique=True),
            IndexModel([("description", 1)], unique=False)           
            ]


class MLFormulationList(BaseModel):
    formulations: list[MLFormulation]

class MLFormulationListPagination(MLFormulationList):
    page: int = Field(ge=1, default=1)
    has_more: bool        

# utility function
async def enrich_formulation(formulation: PreparationFormulation) -> list[Compound]:
    compound_ids = [entry.compound_id for entry in formulation.formulation]
    compounds = await Compound.find(Compound.compound_id.in_(compound_ids)).to_list()
    return compounds


class User(Document):
    username: str = Field(min_length=3, max_length=50)
    password: str
    email: str

    created: datetime = Field(default_factory=datetime.now)

    class Settings:
        name = "user"
            

class RegisterUser(BaseModel):
    username: str
    password: str
    email: str


class LoginUser(BaseModel):
    username: str
    password: str


class CurrentUser(BaseModel):
    username: str
    email: str
    id: PydanticObjectId
