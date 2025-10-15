import React from 'react';
import { usePlotlyChart } from '../../hooks/usePlotlyChart';

const BoxPlot = ({ data }) => {
  const plotData = data.map(group => ({
    y: group.values,
    type: 'box',
    name: group.label,
  }));

  const layout = { title: 'Box Plot', margin: { t: 40 } };
  const ref = usePlotlyChart(plotData, layout);

  return <div ref={ref} />;
};

export default BoxPlot;
