if (!window.dash_clientside) {
    window.dash_clientside = {};
}

function calculatePercentile(arr, percentile) {
    const sorted = arr.slice().sort((a, b) => a - b);
    const index = Math.ceil((percentile / 100) * sorted.length) - 1;
    return sorted[Math.max(0, index)];
}


window.dash_clientside.chart_utils = {

    createCumulativeDistributionChart: function(data, elementId) {
        // Sort the data
        data.sort((a, b) => a - b);
    
        // Calculate the cumulative probabilities
        let cumulativeData = [];
        let cumulativeProbability = 0;
        let n = data.length;
    
        for (let i = 0; i < n; i++) {
            cumulativeProbability += 1 / n;
            cumulativeData.push({
                x: data[i],
                y: cumulativeProbability
            });
        }
    
        // Extract x and y values for the plot
        let xValues = cumulativeData.map(d => d.x);
        let yValues = cumulativeData.map(d => d.y);
    
        // Create the trace for the cumulative distribution chart
        let trace = {
            x: xValues,
            y: yValues,
            mode: 'lines',
            name: 'Cumulative Distribution',
            line: { shape: 'hv' }
        };
    
        // Define the layout for the chart
        let layout = {
            title: 'Cumulative Distribution Chart',
            xaxis: {
              title: 'Return Values (%)',
              tickformat: '.0%'
            },
            yaxis: {
              title: 'Probability',
            },
        };
    
        // Plot the chart using Plotly
        Plotly.newPlot(elementId, [trace], layout);
    }
};