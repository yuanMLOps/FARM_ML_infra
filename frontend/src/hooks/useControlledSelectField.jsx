// useControlledSelectField.tsx

import { useEffect, useState } from "react";
import { Controller } from "react-hook-form";
import Select from "react-select";

// interface UseControlledSelectFieldProps {
//   url: string;
//   arrayName: string;
//   fieldName: string;
//   index: number;
//   control: Control<any>;
//   rules?: RegisterOptions;
//   placeholder?: string;
// }
// 
export const useControlledSelectField = ({
  url,
  arrayName,
  fieldName,
  index,
  control,
  rules = { required: true },
  placeholder = "Select option"
}) => {
  const [options, setOptions] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchOptions = async () => {
      try {
        const res = await fetch(url);
        const data = await res.json();
        const transformed = Array.isArray(data)
          ? data.map(item => ({ label: item, value: item }))
          : data[fieldName]?.map(item => ({ label: item, value: item })) || [];
        setOptions(transformed);
      } catch (err) {
        console.error("Failed to fetch options:", err);
      } finally {
        setLoading(false);
      }
    };
    fetchOptions();
  }, [url, fieldName]);

  const fullName = `${arrayName}.${index}.${fieldName}`;

  return (
    <Controller
      control={control}
      name={fullName}
      rules={rules}
      render={({ field }) => (
        <Select
          options={options}
          isLoading={loading}
          placeholder={placeholder}
          onChange={selected => field.onChange(selected?.value || "")}
          onBlur={field.onBlur}
          value={options.find(opt => opt.value === field.value) || null}
          className="react-select-container"
          classNamePrefix="react-select"
        />
      )}
    />
  );
};
