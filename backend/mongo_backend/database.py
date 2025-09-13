import motor.motor_asyncio
from beanie import init_beanie, Document, PydanticObjectId

from .config import BaseConfig
from .models import (Compound, PreparationFormulation, MLFormulation, 
                     InputFormulation, CompoundEntry)
from typing import Optional, Union 

settings = BaseConfig()


async def init_db():
    client = motor.motor_asyncio.AsyncIOMotorClient(settings.DB_URL)
    await init_beanie(database=client.electrolytes, document_models=[Compound, PreparationFormulation, MLFormulation])

async def bulk_insert(input_list: list, document: Document, 
                      mapping_id_column: Optional[str]=None) -> Union[dict[str, PydanticObjectId], list[PydanticObjectId]]:
    documents = [document(**data) for data in input_list]
    inserted_docs = await document.insert_many(documents)
    if mapping_id_column:
        rs = {
            getattr(doc, mapping_id_column): PydanticObjectId(oid)
            for doc, oid in zip(documents, inserted_docs.inserted_ids)
            }
        return rs
    return inserted_docs.inserted_ids

async def insert_compounds(compound_list: list) -> dict[str, PydanticObjectId]:
    mat_dict = await bulk_insert(compound_list, Compound, "compound_id")
    return mat_dict    

async def insert(input_dict: dict, model: Document, 
                      mapping_id_column: Optional[str]=None) -> Union[dict[str, PydanticObjectId], PydanticObjectId]:
    document = model(**input_dict) 
    inserted_doc = await model.insert_one(document)
    if mapping_id_column:
        rs = {
            getattr(inserted_doc, mapping_id_column): PydanticObjectId(inserted_doc.id)            
            }
        return rs
    return inserted_doc.id

