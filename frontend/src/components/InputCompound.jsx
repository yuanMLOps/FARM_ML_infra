import React from 'react'

const InputCompound = ( props ) => {
   const { index, register, error, onDelete } = props;

    return (
        <div className="compound-entry">
            <input {...register(`formulation.${index}.compound_id`)} type="text" placeholder="Compound id" />
            <input {...register(`formulation.${index}.quantity`)} type = "number" placeholder="%" />
            <select {...register(`formulation.${index}.quantity_type`)} type="text">
            <option value="weight_percent">weight percentage (0-1)</option>
            <option value="volume_percent">volume percentage (0-1)</option>
            <option value="moles">Molarity</option>
            </select>
            <button type="button" onClick={onDelete}>Delete</button>

            {error?.compound_id && <p>{error.compound_id.message}</p>}
            {error?.quantity && <p>{error.quantity.message}</p>}
            {error?.quantity_type && <p>{error.quantity_type.message}</p>}
        </div>
        );
}

export default InputCompound;
