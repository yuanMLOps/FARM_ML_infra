import React from 'react';
import { usePlotlyChart } from '../../hooks/usePlotlyChart';

const BarPlotlyChart = ({ data }) => {
  const plotData = [{
    x: data.map(d => d.label),
    y: data.map(d => d.value),
    type: 'bar',
    marker: { color: 'teal' },
  }];

  const layout = { title: 'Bar Chart', margin: { t: 40 } };
  const ref = usePlotlyChart(plotData, layout);

  return <div ref={ref} />;
};

export default BarPlotlyChart;
