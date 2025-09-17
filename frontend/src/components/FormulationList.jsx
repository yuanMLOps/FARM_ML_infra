import FormulationRow from "./FormulationRow";
const FormulationList = ({ data }) => {
  return (
    <div>
      {data.map((formulation) => (
        <FormulationRow key={formulation.id} formulation={formulation} />
      ))}
    </div>
  );
};



export default FormulationList;
