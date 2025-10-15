
const FormulationRow = ({ formulation }) => {
  return (
    <div className="formulation-card">
      <h3>{formulation.description}</h3>
      <p><strong>Created:</strong> {new Date(formulation.created_at).toLocaleString()}</p>

      <table>
        <thead>
          <tr>
            <th>Compound</th>
            <th>Quantity</th>
            <th>Type</th>
          </tr>
        </thead>
        <tbody>
          {formulation.formulation.map((entry, idx) => (
            <tr key={idx}>
              <td>{entry.compound_id}</td>
              <td>{entry.quantity}</td>
              <td>{entry.quantity_type}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default FormulationRow;