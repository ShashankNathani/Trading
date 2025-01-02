if (!window.dash_clientside) {
    window.dash_clientside = {};
}

function calculatePercentile(arr, percentile) {
    const sorted = arr.slice().sort((a, b) => a - b);
    const index = Math.ceil((percentile / 100) * sorted.length) - 1;
    return sorted[Math.max(0, index)];
}


window.dash_clientside.chart_utils = {

    createProbabilityDistributionChart : function(returns,element_id){

        const sortedReturns = returns.slice().sort((a, b) => a - b);

        // Calculate histogram bins for the probability distribution
        const binCount = 20;
        const minValue = Math.min(...sortedReturns);
        const maxValue = Math.max(...sortedReturns);
        const binSize = (maxValue - minValue) / binCount;
        const bins = Array(binCount).fill(0);
      
        sortedReturns.forEach((value) => {
            const binIndex = Math.min(
            Math.floor((value - minValue) / binSize),
            binCount - 1
            );
            bins[binIndex]++;
        });
      
        // Normalize bin counts to get probabilities
        const probabilities = bins.map((count) => count / sortedReturns.length);

        // Calculate bin centers for the x-axis and convert to percentages
        const binCenters = bins.map((_, i) => (minValue + i * binSize + binSize / 2) / maxValue );
      
        // Calculate percentile values
        const percentiles = [5, 10, 15, 20, 80, 85, 90, 95].map((p) => {
          return {
            percentile: p,
            value: calculatePercentile(sortedReturns, p),
            };
        });
      
        const histogramTrace = {
          x: binCenters,
          y: probabilities,
          type: 'bar',
          name: 'Probability Distribution',
          marker: {
            color: 'rgba(75, 192, 192, 0.6)',
            },
        };
      
        // Create traces for percentile lines
        const percentileTraces = percentiles.map((p) => ({
          x: [p.value / maxValue, p.value / maxValue],
          y: [0, Math.max(...probabilities)],
          type: 'scatter',
          mode: 'lines',
          name: `${p.percentile}th Percentile`,
          line: {
            color: 'rgba(255, 99, 132, 0.8)',
            width: 2,
            dash: 'dash',
          },
        }));
      
        // Combine all traces
        const data = [histogramTrace, ...percentileTraces];
      
        // Layout configuration
        const layout = {
          title: 'Probability Distribution Chart',
          xaxis: {
            title: 'Return Values (%)',
            tickformat: '.0%'
          },
          yaxis: {
            title: 'Probability',
          },
          barmode: 'overlay',
        };
      
        Plotly.react(element_id, data, layout);
    }
};