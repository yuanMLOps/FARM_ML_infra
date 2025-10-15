import React from 'react';
import { usePlotlyChart } from '../../hooks/usePlotlyChart';

const ScatterPlotlyPlot = ({ data }) => {
  const plotData = [{
    x: data.map(d => d.x),
    y: data.map(d => d.y),
    mode: 'markers',
    type: 'scatter',
    marker: { color: 'blue' },
  }];

  const layout = { title: 'Scatter Plot', margin: { t: 40 } };
  const ref = usePlotlyChart(plotData, layout);

  return <div ref={ref} />;
};

export default ScatterPlotlyPlot;
