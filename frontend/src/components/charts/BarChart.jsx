import { useCallback } from 'react';
import { useD3Chart } from '../../hooks/useD3Chart';
import * as d3 from 'd3';

const BarChart = ({ data , width = 400, height = 300} ) => {
     const renderChart = useCallback((container) => {
      d3.select(container).selectAll('*').remove();
  
      const svg = d3.select(container)
        .append('svg')
        .attr('width', width)
        .attr('height', height);
  
      const x = d3.scaleBand()
        .domain(data.map(d => d.label))
        .range([40, width - 20])
        .padding(0.1);
  
      const y = d3.scaleLinear()
        .domain([0, d3.max(data, d => d.value)])
        .range([height - 30, 20]);
  
      svg.selectAll('rect')
        .data(data)
        .join('rect')
        .attr('x', d => x(d.label))
        .attr('y', d => y(d.value))
        .attr('width', x.bandwidth())
        .attr('height', d => height - 30 - y(d.value))
        .attr('fill', 'teal');
     }, [data, width, height]);

      const ref = useD3Chart(renderChart, data, width, height);
   
      return <div ref={ref} />;
  }

  export default BarChart
  


