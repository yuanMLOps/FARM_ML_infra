import { useCallback} from 'react';
import { useD3Chart } from '../../hooks/useD3Chart';
import * as d3 from 'd3';

const ScatterPlot = ({ data, width = 400, height = 300 }) => {
  const renderChart = useCallback((container) => {
    const svg = d3.select(container)
      .append('svg')
      .attr('width', width)
      .attr('height', height);

    const x = d3.scaleLinear().domain([0, 100]).range([40, width - 20]);
    const y = d3.scaleLinear().domain([0, 100]).range([height - 30, 20]);

    svg.selectAll('circle')
      .data(data)
      .join('circle')
      .attr('cx', d => x(d.x))
      .attr('cy', d => y(d.y))
      .attr('r', 5)
      .attr('fill', 'steelblue');
  }, [data, width, height]);

  const ref = useD3Chart(renderChart, data, width, height);

  return <div ref={ref} />;
};

export default ScatterPlot;
