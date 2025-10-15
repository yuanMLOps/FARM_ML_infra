import React from 'react'
import { useControlledSelectField } from "../hooks/useControlledSelectField"; 

const url = `${import.meta.env.VITE_API_URL}/formulations/compound_ids`;
const arrayName = "formulation";
const fieldName = "compound_id";



const InputCompoundHook = ( props) => {
  const { index, register, control, error, onDelete } = props; 
  return (
    <div className="mb-6 p-4 border rounded-lg shadow-sm bg-white space-y-4">
      {/* Compound ID Select */}
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-1">Compound ID</label>
        {useControlledSelectField({ url, arrayName, fieldName, index, control})}
      </div>

      {/* Quantity Input */}
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-1">Quantity (%)</label>
        <input
          {...register(`formulation.${index}.quantity`)}
          type="number"
          step={0.001}
          placeholder="e.g. 25"
          className="w-full px-3 py-2 border rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
        {error?.quantity && (
          <p className="text-red-500 text-xs mt-1">{error.quantity.message}</p>
        )}
      </div>

      {/* Quantity Type Select */}
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-1">Quantity Type</label>
        <select type="text"
          {...register(`formulation.${index}.quantity_type`)}
          className="w-full px-3 py-2 border rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
        >
          <option value="weight_percent">Weight % (0–1)</option>
          <option value="volume_percent">Volume % (0–1)</option>
          <option value="moles">Molarity</option>
        </select>
        {error?.quantity_type && (
          <p className="text-red-500 text-xs mt-1">{error.quantity_type.message}</p>
        )}
      </div>

      {/* Delete Button */}
      <div className="flex justify-end">
        <button
          type="button"
          onClick={onDelete}
          className="text-sm text-red-600 hover:text-red-800 font-medium"
        >
          Delete
        </button>
      </div>
    </div>
  );
};
  

export default InputCompoundHook