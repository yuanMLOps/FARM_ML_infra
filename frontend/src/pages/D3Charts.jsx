import { useState } from 'react';
import ScatterPlot from '../components/charts/ScatterPlot';
import BarChart from '../components/charts/BarChart';
import RadialChart from '../components/charts/RadialChart';

const D3Charts = () => {
  const [scatterData, setScatterData] = useState([
    { x: 12, y: 34 },
    { x: 45, y: 22 },
    { x: 33, y: 55 },
    { x: 60, y: 40 },
    { x: 80, y: 70 },
  ]);

  const [barData, setBarData] = useState([
    { label: 'Apples', value: 30 },
    { label: 'Bananas', value: 45 },
    { label: 'Cherries', value: 25 },
    { label: 'Dates', value: 60 },
    { label: 'Elderberries', value: 40 },
  ]);

  const [radialData, setRadialData] = useState([
    { label: 'Chrome', value: 55 },
    { label: 'Firefox', value: 20 },
    { label: 'Safari', value: 15 },
    { label: 'Edge', value: 10 },
  ]);

  // Example: simulate data update
  const updateBarData = () => {
    setBarData(barData.map(d => ({
      ...d,
      value: Math.floor(Math.random() * 100)
    })));
  };

  return (
    <div>
      <h2>Scatter Plot</h2>
      <ScatterPlot data={scatterData} />

      <h2>Bar Chart</h2>
      <BarChart data={barData} />
      <button onClick={updateBarData}>Update Bar Data</button> 
      <h2>Radial Chart</h2>
      <RadialChart data={radialData} radius={200} />
    </div>
  );
};

export default D3Charts;
