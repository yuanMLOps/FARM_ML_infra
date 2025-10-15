import React from 'react';
import { usePlotlyChart } from '../../hooks/usePlotlyChart';

const LineChart = ({ data }) => {
  const plotData = [{
    x: data.map(d => d.x),
    y: data.map(d => d.y),
    type: 'scatter',
    mode: 'lines+markers',
    line: { shape: 'spline', color: 'orange' },
  }];

  const layout = { title: 'Line Chart', margin: { t: 40 } };
  const ref = usePlotlyChart(plotData, layout);

  return <div ref={ref} />;
};

export default LineChart;
