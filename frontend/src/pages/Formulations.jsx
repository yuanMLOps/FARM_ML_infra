import React from 'react'
import { useLoaderData } from "react-router-dom"
import FormulationList from "../components/FormulationList"

const Formulations = () => {
  const formulations = useLoaderData()
  console.log("Fetched formulations:", formulations);

  return (
    <div>
        <FormulationList data={formulations} />
    </div>
  )
}

export default Formulations

