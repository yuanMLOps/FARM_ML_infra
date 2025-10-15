import { z } from 'zod';
import { useForm, useFieldArray } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { useNavigate } from "react-router-dom";

import { useAuth } from "../hooks/useAuth";
import InputFormulationField from "../components/InputFormulationField";
import InputCompoundSelect from "../components/InputCompoundSelect";
import InputCompoundHook from '../components/InputCompoundHook';

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
  cycle: z.coerce.number().gte(0).optional(),
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

  let formArray = [

        {
            name: "description",
            type: "text",
            error: errors.description,
            required: true
        },

        {
            name: "CE",
            type: "number",
            error: errors.CE,
            step: 0.0001,
            required: false
        },
        {
            name: "LCE",
            type: "number",
            error: errors.LCE,
            step: 0.01,
            required: false
        },
        
        {
            name: "cycle",
            type: "number",
            error: errors.cycle,
            required: false
        },
        {
            name: "current",
            type: "number",
            step: 0.001,
            error: errors.current,
            required: false
        },
        {
            name: "capacity",
            type: "number",
            step: 0.01,
            error: errors.capacity,
            required: false
        },
        

    ]

  return (
    <form onSubmit={ handleSubmit(onSubmit, (errors) => console.log("Validation errors:", errors))}>
      <h2>Insert New Formulation</h2>

      {formArray.map((item) => (
        <InputFormulationField 
           key={item.name}
           name={item.name}
           type={item.type} 
           error={item.error} 
           register={register}
           required={item.required}
           {...(item.step !== undefined ? { step: item.step } : {})}

           />

       ) )
      }

      {/* <InputFormulationField name="description" type="text" error={errors.description} register = {register} />
      <InputFormulationField name="CE" type="number" error={errors.CE} register={register} /> */}

      <h3>Compounds</h3>
      {fields.map((field, index) => (
        // <InputCompoundSelect
        <InputCompoundHook
          key={field.id}
          index={index}
          register={register}
          control={control}
          error={errors.formulation?.[index]}
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

