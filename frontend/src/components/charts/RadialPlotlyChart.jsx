import React from 'react';
import { usePlotlyChart } from '../../hooks/usePlotlyChart';

const RadialPlotlyChart = ({ data }) => {
  const plotData = [{
    labels: data.map(d => d.label),
    values: data.map(d => d.value),
    type: 'pie',
  }];

  const layout = { title: 'Radial Chart', margin: { t: 40 } };
  const ref = usePlotlyChart(plotData, layout);

  return <div ref={ref} />;
};

export default RadialPlotlyChart;
