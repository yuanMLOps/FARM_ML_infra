import React from 'react'

const InputFormulationField = ( props ) => {
  const { name, type, error, register, required, step } = props
    return (

        <div className="mb-4">
            <label className="block text-gray-700 text-sm font-bold mb-2" htmlFor={name}>
                {name}
            </label>
            <input
                className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                id={name}
                name={name}
                type={type}
                required={required}
                step={step ?? "any"}
                placeholder={name}
              
                autoComplete="off"
                {...register(name)}
            />
            {error && <p className="text-red-500 text-xs italic">{error.message}</p>}
        </div>
    )
}
 

export default InputFormulationField