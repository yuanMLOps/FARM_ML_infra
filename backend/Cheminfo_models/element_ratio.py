from collections import defaultdict
from rdkit.Chem import AllChem, Descriptors
from typing import Dict, Tuple
from collections import defaultdict

from rdkit import Chem
import pubchempy as pcp

class SMILESExcept(Exception):
    def __init__(self, message):
        super().__init__(message)


class CompoundIDExcept(Exception):
    def __init_(self, message):
        super().__init__(message)       

def count_atoms(smiles_string):
    '''
    Given a SMILES string and a list of atoms to count, return a dictionary of atoms to respective counts.
    '''

    atom_counts = defaultdict(int)
        
    try:
        molecule = Chem.MolFromSmiles(smiles_string)
        if molecule is None:
            raise Exception()
        molecule = Chem.AddHs(molecule)

        for atom in molecule.GetAtoms():
            atom_symbol = atom.GetSymbol()
            # if atom_symbol in atom_set:
            atom_counts[atom_symbol] += 1
                
        return atom_counts         
        
    except Exception as e:
        print(f"Error processing SMILES string in atom_counts: {smiles_string}")
        #print(e)
        return {}

def calculate_molar_volume(sm_str: str) -> float:

    try:
        molecule = Chem.MolFromSmiles(sm_str)
        if molecule is None:
            raise Exception()
            
        molecule = Chem.AddHs(molecule)
        AllChem.EmbedMolecule(molecule)

        # Calculate the molar volume
        mol_volume = AllChem.ComputeMolVolume(molecule)
                
        return mol_volume      
        
    except Exception as e:
        print(f"Error processing SMILES string in molar volume: {sm_str}")
        raise SMILESExcept(f"invalid SMILES string: {sm_str}")    

def get_solvent_type(sm_str: str) -> str:
    try:
        mol = Chem.MolFromSmiles(sm_str)
    except Exception as e:
        print(f"Invalid SMILES string {sm_str}")
        raise SMILESExcept(f"input string is {sm_str}")
    
    # Check for charges
    try:
        for atom in mol.GetAtoms():
            if atom.GetFormalCharge() != 0:
                return "Salt"
    except Exception as e:
        print(f"Invalid SMILES string {sm_str}")
        raise SMILESExcept(f"input string is {sm_str}")        
    
    return "Solvent"   


def get_smiles_from_chem_formula(formula: str) -> Tuple[str, str]:
    # Replace 'molecule_name' with the actual name of the molecule
    
    try:
        compounds = pcp.get_compounds(formula, 'name')    
        props =  compounds[0]._record['props']

        for prop in props:
            if prop['urn']['label'] == "SMILES" and prop['urn']['name'] == 'Absolute':
                canonical_smiles = prop['value']['sval'] 
        formula = compounds[0].molecular_formula
    except Exception as e:
        # print(f"No compound found with the given IUPAC name.{formula}")
        raise CompoundIDExcept(f"No compound found with the given IUPAC name.{formula}")
        
        # print(f"Canonical SMILES: {canonical_smiles}")
    return canonical_smiles, formula   


def calculate_molar_mass(sm_str: str) -> float:

    try:
        molecule = Chem.MolFromSmiles(sm_str)
    except Exception as e:
        print(f"Error processing SMILES string in molar mass: {sm_str}")
        raise SMILESExcept(f"input string is {sm_str}")       
          
    mol_mass = Descriptors.MolWt(molecule)
            
    return mol_mass     

def construct_compound_from_chem_formula(formula: str) -> Dict[str, str]:
    rs = dict()

    smiles_str, formula = get_smiles_from_chem_formula(formula)

    rs["Chem_Formula"] = formula
    rs["SMILES"] = smiles_str
    rs["Solvent_Type"] =  get_solvent_type(smiles_str)
    rs["Molar_Mass"] = calculate_molar_mass(smiles_str)
    
    return rs

def calculate_element_ratios_by_moles(mole_lists: list[float], 
                                      smiles_list: list[str], solvent_list: list[str] ) -> dict:
    element_moles = defaultdict(float)

    for moles, smiles_str, solvent_type in zip(mole_lists, smiles_list, solvent_list):
        
        atom_counts = count_atoms(smiles_str)

        for atom in atom_counts:
            atom_moles = moles * atom_counts[atom]
            element_moles[atom] += atom_moles

            # add total moles of atoms to "total_moles"
            element_moles["total_moles"] += atom_moles

            if solvent_type == "Solvent":
                element_moles["solvent_moles"] += atom_moles
                if atom == 'O':
                    element_moles["oxygen_solvent_moles"] += atom_moles
                elif atom == 'C':
                    element_moles["carbon_solvent_moles"] += atom_moles
                elif atom == 'F':
                    element_moles["florine_solvent_moles"] += atom_moles

            elif solvent_type == "Salt":
                element_moles["salt_moles"] += atom_moles
                if atom == 'O':
                    element_moles["oxygen_anion_moles"] += atom_moles
                elif atom == 'C':
                    element_moles["carbon_anion_moles"] += atom_moles
                elif atom == 'F':
                    element_moles["florine_anion_moles"] += atom_moles

    element_moles["organic_moles"] = element_moles["C"] 
    # element_moles["inorganic_moles"] = element_moles["total_moles"] - element_moles["C"] - element_moles["H"]
    element_moles["inorganic_moles"] = element_moles["total_moles"] - element_moles["C"] - element_moles["H"] - element_moles["Li"]
    total = element_moles["total_moles"]
    
    element_ratios = defaultdict(float)

    element_ratios["FC"] = element_moles["F"] / element_moles["C"]
    element_ratios["OC"] = element_moles["O"] / element_moles["C"]
    element_ratios["FO"] = element_moles["F"] / element_moles["O"]
    element_ratios["InOr"] = element_moles["inorganic_moles"] / element_moles["organic_moles"]

    element_ratios["F"] = element_moles["F"] / total
    element_ratios["sF"] = element_moles["florine_solvent_moles"] / total
    element_ratios["aF"] = element_moles["florine_anion_moles"] / total
    
    
    element_ratios["O"] = element_moles["O"] / total
    element_ratios["sO"] = element_moles["oxygen_solvent_moles"] / total
    element_ratios["aO"] = element_moles["oxygen_anion_moles"] / total

    element_ratios["C"] = element_moles["C"] / total
    element_ratios["sC"] = element_moles["carbon_solvent_moles"] / total
    element_ratios["aC"] = element_moles["carbon_anion_moles"] / total
    # element_ratios.update(element_moles)   

    return element_ratios