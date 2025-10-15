import { useState } from 'react';
import ScatterPlotlyPlot from '../components/charts/ScatterPlotlyPlot';
import BarPlotlyChart from '../components/charts/BarPlotlyChart';
import RadialPlotlyChart from '../components/charts/RadialPlotlyChart';
import LineChart from '../components/charts/LineChart';
import BoxPlot from '../components/charts/BoxPlot';

const PlotlyCharts = () => {
  const [scatterData, setScatterData] = useState([
    { x: 10, y: 20 }, { x: 30, y: 40 }, { x: 50, y: 60 }
  ]);

  const [barData, setBarData] = useState([
    { label: 'A', value: 20 }, { label: 'B', value: 35 }, { label: 'C', value: 50 }
  ]);

  const [radialData, setRadialData] = useState([
    { label: 'X', value: 40 }, { label: 'Y', value: 30 }, { label: 'Z', value: 30 }
  ]);

  const [lineData, setLineData] = useState([
    { x: 1, y: 10 }, { x: 2, y: 15 }, { x: 3, y: 12 }, { x: 4, y: 18 }
  ]);

  const [boxData, setBoxData] = useState([
    { label: 'Group A', values: [10, 20, 15, 25, 18] },
    { label: 'Group B', values: [22, 28, 26, 30, 24] }
  ]);

  return (
    <div>
      <h2>Scatter Plot</h2>
      <ScatterPlotlyPlot data={scatterData} />

      <h2>Bar Chart</h2>
      <BarPlotlyChart data={barData} />

      <h2>Radial Chart</h2>
      <RadialPlotlyChart data={radialData} />

      <h2>Line Chart</h2>
      <LineChart data={lineData} />

      <h2>Box Plot</h2>
      <BoxPlot data={boxData} />
    </div>
  );
};

export default PlotlyCharts;


