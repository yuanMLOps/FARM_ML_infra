from fastapi import APIRouter, BackgroundTasks, Body, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from beanie import PydanticObjectId

from ..authentication import AuthHandler
from mongo_backend import (PreparationFormulation, MLFormulation, CompoundEntry, 
                           Compound, ElementRatio, InputFormulation, PreparationFormulationListPagination,
                           MLFormulationListPagination, UpdateFormulation)
from Cheminfo_models import calculate_element_ratios_by_moles


auth_handler = AuthHandler()
FORMULATIONS_PER_PAGE = 10

router = APIRouter()


@router.post("/", response_model=MLFormulation, status_code=status.HTTP_201_CREATED)
async def add_formulation(input_form: InputFormulation=Body(...)):
    
    # Build formulation entries
    prep_formulation = []
    ml_formulation = []
    smiles_list, mole_list, solvent_list = [], [], []
    
    for entry in input_form.formulation:
        compound_id = entry.compound_id
        compound_doc = await Compound.find_one({"compound_id": compound_id})
        if not compound_doc:
            raise HTTPException(status_code=404, detail=f"Compound {compound_id} not found")

        # construct the smiles_list, moles_list, solvent_list for element ratio calculation
        smiles_list.append(compound_doc.SMILES)
        solvent_list.append(compound_doc.Solvent_Type)

        # Construct Link[Compound] manually
        quantity = entry.quantity
        quantity_type = entry.quantity_type
        prep_formulation.append(
            CompoundEntry(
                compound=compound_doc.id,
                compound_id=compound_id,
                quantity=quantity,
                quantity_type=quantity_type
            )
        )

        if quantity_type == "weight_percent":
            ml_quantity = quantity * 1000 / compound_doc.Molar_Mass
        elif quantity_type == "volume_percent": 
            ml_quantity = quantity * 1000 * compound_doc.Density / compound_doc.Molar_Mass
        else:
            ml_quantity = quantity 

        mole_list.append(ml_quantity)                  

        ml_formulation.append(
            CompoundEntry(
                compound=compound_doc.id,
                compound_id=compound_id,
                quantity=ml_quantity,
                quantity_type="moles"
            )
        )      
       

    # Create and save PreparationFormulation
    prep_form = PreparationFormulation(
        description=input_form.description,
        formulation=prep_formulation
    )
    saved_prep = await prep_form.save()
    prep_id = saved_prep.id

    element_ratio_calculated = calculate_element_ratios_by_moles(mole_list, smiles_list, solvent_list) 
    ml_element_ratio = ElementRatio(**element_ratio_calculated)
    
    ml_form = MLFormulation(
        preparation_id=prep_id,
        description=input_form.description,
        formulation=ml_formulation,
        element_ratio=ml_element_ratio
    )

    saved_ml = await ml_form.save()
    return saved_ml


@router.get(
    "/prep_formulations",
    response_description="List all formulations, paginated",
    response_model=PreparationFormulationListPagination,
    response_model_by_alias=False,
)
async def list_prep_formulations(
    # user=Depends(auth_handler.auth_wrapper),
    page: int = 1,
    limit: int = FORMULATIONS_PER_PAGE,
):
    prep_docs = await PreparationFormulation.find().limit(limit).skip((page - 1) * limit).to_list()

    total_documents = await PreparationFormulation.find().count()
    has_more = total_documents > limit * page
    
    return PreparationFormulationListPagination(formulations=prep_docs, page=page, has_more=has_more)


@router.get(
    "/ml_formulations",
    response_description="List all moles formulations, paginated",
    response_model=MLFormulationListPagination,
    response_model_by_alias=False,
)
async def list_ml_formulations(
    # user=Depends(auth_handler.auth_wrapper),
    page: int = 1,
    limit: int = FORMULATIONS_PER_PAGE,
):
    ml_docs = await MLFormulation.find().limit(limit).skip((page - 1) * limit).to_list()

    total_documents = await MLFormulation.find().count()
    has_more = total_documents > limit * page
    
    return MLFormulationListPagination(formulations=ml_docs, page=page, has_more=has_more)


@router.put("/{prep_form_id}", response_model=MLFormulation)
async def update_formulation(prep_form_id: PydanticObjectId, formulation_data: UpdateFormulation):

    prep_form = await PreparationFormulation.get(prep_form_id)
    if not prep_form:
        raise HTTPException(status_code=404, detail="preparation formulation not found")
    ml_form = await MLFormulation.find_one(MLFormulation.preparation_id.id == prep_form_id)
    if not ml_form:
        raise HTTPException(status_code=404, detail="calculated machine learning formulation not found")
    
    if not formulation_data.formulation:
        update_dict = formulation_data.model_dump(exclude_none=True)
        print(f"update_dict={update_dict}")
        if "description" in update_dict.keys():
            await prep_form.set({"description": update_dict["description"]})
        await ml_form.set(update_dict)
        return ml_form

    # Build formulation entries
    prep_formulation = []
    ml_formulation = []
    smiles_list, mole_list, solvent_list = [], [], []
    
    for entry in formulation_data.formulation:
        compound_id = entry.compound_id
        compound_doc = await Compound.find_one({"compound_id": compound_id})
        if not compound_doc:
            raise HTTPException(status_code=404, detail=f"Compound {compound_id} not found")

        # construct the smiles_list, moles_list, solvent_list for element ratio calculation
        smiles_list.append(compound_doc.SMILES)
        solvent_list.append(compound_doc.Solvent_Type)

        # Construct Link[Compound] manually
        quantity = entry.quantity
        quantity_type = entry.quantity_type
        prep_formulation.append(
            CompoundEntry(
                compound=compound_doc.id,
                compound_id=compound_id,
                quantity=quantity,
                quantity_type=quantity_type
            )
        )

        if quantity_type == "weight_percent":
            ml_quantity = quantity * 1000 / compound_doc.Molar_Mass
        elif quantity_type == "volume_percent": 
            ml_quantity = quantity * 1000 * compound_doc.Density / compound_doc.Molar_Mass
        else:
            ml_quantity = quantity 

        mole_list.append(ml_quantity)                  

        ml_formulation.append(
            CompoundEntry(
                compound=compound_doc.id,
                compound_id=compound_id,
                quantity=ml_quantity,
                quantity_type="moles"
            )
        )      
    

    # Create and save PreparationFormulation
    prep_update = formulation_data.model_dump(exclude={"formulation"}, exclude_none=True)
    await prep_form.set({"description": prep_update["description"]})
    
    await prep_form.set({"formulation":  [entry.model_dump() for entry in prep_formulation]})
    
    element_ratio_calculated = calculate_element_ratios_by_moles(mole_list, smiles_list, solvent_list) 
    ml_element_ratio = ElementRatio(**element_ratio_calculated)
    
    await ml_form.set(prep_update)
    await ml_form.set(
        {"formulation": [entry.model_dump() for entry in ml_formulation],
         "element_ratio": ml_element_ratio.model_dump()
        }     
    )

    return ml_form


@router.delete("/{prep_form_id}")
async def delete_formulation(prep_form_id: PydanticObjectId):
    prep_form = await PreparationFormulation.get(prep_form_id)
    if not prep_form:
        raise HTTPException(status_code=404, detail="preparation formulation not found")
    ml_form = await MLFormulation.find_one(MLFormulation.preparation_id.id == prep_form_id)
    if not ml_form:
        raise HTTPException(status_code=404, detail="calculated machine learning formulation not found")
    
    await prep_form.delete()
    await ml_form.delete()
    