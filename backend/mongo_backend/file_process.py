from pandas import DataFrame
import pandas as pd
from beanie import PydanticObjectId
from .database import bulk_insert, insert
from .models import Compound, PreparationFormulation, MLFormulation


def construct_formulation_list_from_df(input_df: DataFrame, solvent_type: str) -> list:
    rs_list = []
    solvent_suffix = ""
    if solvent_type == "volume_percent":
        solvent_suffix = "_Volume_Percent"
    elif solvent_type == "weight_percent":
        solvent_suffix = "_Weight_Percent"
    elif solvent_type == "moles":
        solvent_suffix = "_Molarity"

    for i, row in input_df.iterrows():
        electrolyte = dict()
        electrolyte['formulation'] = []
        electrolyte['description'] = row['Description']
        for i in range(1, 4):
            solvent_col = 'Solvent ' + str(i)
            if not pd.isna(row[solvent_col]):
                solvent_quantity_col = solvent_col + solvent_suffix
                electrolyte['formulation'].append({'compound_id': row[solvent_col], 
                                               'quantity': row[solvent_quantity_col], 'quantity_type': solvent_type})
            salt_col = 'Salt ' + str(i)
            if not pd.isna(row[salt_col]):
                salt_quantity_col = salt_col + "_Molarity"
                electrolyte['formulation'].append({'compound_id': row[salt_col], 
                                               'quantity': row[salt_quantity_col], 'quantity_type': "moles"})         
        rs_list.append(electrolyte) 
    return rs_list


def construct_MLformulation_list_from_df(input_df: DataFrame) -> list:
    element_ratio_columns = ['FC', 'OC', 'FO', 'InOr', 'F', 'sF', 'aF', 'O', 'sO',
       'aO', 'C', 'sC', 'aC']
    mole_prep_formulation_list = construct_formulation_list_from_df(input_df, "moles")
    property_dict = {'CE': 'CE (%)', 'LCE': 'LCE', 'current': 'Current (mA/cm2)', 'capacity': 'Capacity (mAh/cm2)', 'cycle': 'Cycle'}
    
    
    for i, row in input_df.iterrows():
        mole_prep_formulation_list[i]['element_ratio'] = dict()
        for col in element_ratio_columns:
            mole_prep_formulation_list[i]['element_ratio'][col] = row[col]
        for col in property_dict.keys():
            val = row[property_dict[col]]
            if not pd.isna(val):
                mole_prep_formulation_list[i][col] = val        
    return mole_prep_formulation_list                                                        
    

def add_id_to_list(object_list: list, id_column: str, associated_id_column: str, id_dict: dict[str, PydanticObjectId]) -> None:
    """
    This function adds the associated PydanticObjectId to the input list based on the id_column(ObjectId Link column name) and
    associated_id_column (the key in the id_dict that associates the associated_id_column value of objects in object_list)
    to summarize, id_column is Link column(such as compound), and associated_id_column is the source column such as compound_id
    """
    for ob in object_list:
        ob[id_column] = id_dict[ob[associated_id_column]]
   

def construct_preparation_formulation_list(electrolyte_list: list, id_dict: dict[str, PydanticObjectId]) -> None:
    """
    This function modifies the input electrolyte_list by adding the corresponding PydanticObjectId to each compound of the formulation
    list. 
    """
    for electrolyte in electrolyte_list:
        add_id_to_list(electrolyte["formulation"], "compound", "compound_id", id_dict)


def construct_MLFormulation_list(electrolyte_list: list, compound_id_dict: dict[str, PydanticObjectId],
                                 prep_id_list: list[PydanticObjectId]) -> None:
    """
    This function modifies the input electrolyte_list by adding the corresponding PydanticObjectId to each compound of the formulation
    list and preparation_id, and construct the MLFormulation list. Note even if we don't construct rs list, the input list already 
    be modified for batch insert. The rs list is only to check each MLFormulation object can be constructed without errors.
    """
    
    for i, electrolyte in enumerate(electrolyte_list):
        add_id_to_list(electrolyte["formulation"], "compound", "compound_id", compound_id_dict)
        electrolyte["preparation_id"] = prep_id_list[i]   


async def insert_preparation_ML_formulations(prep_list: list, ml_list: list, mat_dict: dict) -> dict[PydanticObjectId, PydanticObjectId]:
    try:
        # modify the input prep_list
        construct_preparation_formulation_list(prep_list, mat_dict) 
        # insert prepformulation 
        prep_formula_list = await bulk_insert(prep_list, PreparationFormulation)
        # modify the input ML_list
        construct_MLFormulation_list(ml_list, mat_dict, prep_formula_list)
        # insert MLFormulations
        MLFormulation_list = await bulk_insert(ml_list, MLFormulation)
        return {prep_form: ml_form for (prep_form, ml_form) in zip(prep_formula_list, MLFormulation_list)}
    except Exception as e:
        print(f"Insert failed: {e}")
        return {"error": str(e)}      

async def insert_one_formulation(prep_form: dict, ml_form: dict, mat_dict: dict) -> PydanticObjectId:
          try:                      
            add_id_to_list(prep_form["formulation"], "compound", "compound_id", mat_dict) 
            prep_id = await insert(prep_form, PreparationFormulation)

            add_id_to_list(ml_form["formulation"], "compound", "compound_id", mat_dict)
            ml_form["preparation_id"] = prep_id
            ml_id = await insert(ml_form, MLFormulation)

            return ml_id
          except Exception as e:
              print(f"Insert failed: {e}")
              return {"error": str(e)}   
              
            

