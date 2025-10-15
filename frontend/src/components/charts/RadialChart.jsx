import * as d3 from 'd3';
import { useCallback } from 'react'
import { useD3Chart } from '../../hooks/useD3Chart'

const RadialChart1 = ({data, radius = 150} ) => {
    // console.log("radius", radius);
  
  const renderChart = useCallback((container) =>{
  
    d3.select(container).selectAll('*').remove();

    const svg = d3.select(container)
      .append('svg')
      .attr('width', radius * 2)
      .attr('height', radius * 2)
      .append('g')
      .attr('transform', `translate(${radius},${radius})`);

    const pie = d3.pie().value(d => d.value);
    const arc = d3.arc().innerRadius(0).outerRadius(radius);

    svg.selectAll('path')
      .data(pie(data))
      .join('path')
      .attr('d', arc)
      .attr('fill', (d, i) => d3.schemeCategory10[i % 10])
      .attr('stroke', '#fff')
      .attr('stroke-width', 1);
  }, [data, radius]);

  const ref = useD3Chart(renderChart, data, null, null, radius);
  return  <div ref={ref} />;
}

export default RadialChart1
