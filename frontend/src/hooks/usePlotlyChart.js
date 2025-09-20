import { useEffect, useRef } from 'react';
import Plotly from 'plotly.js-dist-min';

export function usePlotlyChart(data, layout, config = {}) {
  const ref = useRef();

  useEffect(() => {
    if (!ref.current) return;

    Plotly.newPlot(ref.current, data, layout, config);

    return () => {
      if (ref.current) {
        Plotly.purge(ref.current); // ✅ Only purge if DOM node exists
      }
    };
  }, [data, layout]);

  return ref;
}

