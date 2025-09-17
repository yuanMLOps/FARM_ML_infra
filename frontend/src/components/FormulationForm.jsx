import { z } from 'zod';
import { useForm, useFieldArray } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { useNavigate } from "react-router-dom";

import { useAuth } from "../hooks/useAuth";
import InputFormulationField from "../components/InputFormulationField";
import InputCompound from "../components/InputCompound";

const compoundSchema = z.object({
  compound_id: z.string().min(1),
  quantity: z.coerce.number().gte(0).lte(100),
  quantity_type: z.enum(['weight_percent', 'volume_percent', 'moles']),
});

const formulationSchema = z.object({
  description: z.string().min(2),
  formulation: z.array(compoundSchema).min(1),
  CE: z.coerce.number().gte(0).lte(100).optional(),
  LCE: z.coerce.number().gte(0).lte(10).optional(),
  cycle: z.coerce.number().gt(0).optional(),
  current: z.coerce.number().gte(0).optional(),
  capacity: z.coerce.number().gte(0).optional()
});



const FormulationForm = () => {
  const navigate = useNavigate();
  const { jwt, setMessage } = useAuth();

  const { register, control, handleSubmit, formState: { errors, isSubmitting } } = useForm({
    resolver: zodResolver(formulationSchema),
    defaultValues: {
      formulation: [{ compound_id: "", quantity: 0, quantity_type: "volume_percent" }]
    }
  });

  const { fields, append, remove } = useFieldArray({
    control,
    name: "formulation"
  });

  const onSubmit = async (data) => {
    console.log("start sending request");
    console.log(data);
    console.log(JSON.stringify(data));

    const result = await fetch(`${import.meta.env.VITE_API_URL}/formulations/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${jwt}`,
      },
      body: JSON.stringify(data)
    });

    const json = await result.json();

    if (result.ok) {
      navigate('/formulations');
    } else if (json.detail) {
      setMessage(JSON.stringify(json));
      navigate('/');
    }
  };

  return (
    <form onSubmit={ handleSubmit(onSubmit, (errors) => console.log("Validation errors:", errors))}>
      <h2>Insert New Car</h2>

      <InputFormulationField name="description" type="text" error={errors.description} register = {register} />
      <InputFormulationField name="CE" type="number" error={errors.CE} register={register} />

      <h3>Compounds</h3>
      {fields.map((field, index) => (
        <InputCompound
          key={field.id}
          index={index}
          register={register}
          error={errors.compounds?.[index]}
          onDelete={() => remove(index)}
        />
      ))}

      <button type="button" onClick={() => append({ name: "", percentage: 0, type: "mass" })}>
        Add Compound
      </button>

      <button type="submit"> Submit New Formulation </button>    

      {/* <button type="submit" disabled={isSubmitting}>
        {isSubmitting ? "Saving..." : "Save"}
      </button> */}
    </form>
  );
};

export default FormulationForm;

