import { useEffect, useRef } from 'react';
import * as d3 from 'd3';

export function useD3Chart(renderFn, data, width=null, height=null, radius=null) {
  const ref = useRef();

  useEffect(() => {
    const container = ref.current;
    d3.select(container).selectAll('*').remove(); // 🧼 Clean up before re-render
    renderFn(ref.current);
  }, [renderFn, data, width, height, radius]); // 🔁 Re-run when dependencies change

  return ref;
}
