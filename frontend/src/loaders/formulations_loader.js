export const formulationsLoader = async () => {

    const res = await fetch(`${import.meta.env.VITE_API_URL}/formulations/prep_formulations?limit=10`)
    //const res = await fetch('http://localhost:8000/formulations/prep_formulations?limit=10')

    const response = await res.json()

    if (!res.ok) {
        throw new Error(response.message)
    }
    // console.log("Fetched formulations:", response.formulations);

    return response.formulations
}

