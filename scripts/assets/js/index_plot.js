$(document).ready(function(){
var traceCA = {
  x: ['Default', 'SHREC', 'Loudun 1', 'Empire', 'Lans', 'Church', 'Pisa Cathedral', 'Euler', 'Munich', 'Train st.', 'Loudun 35', 'ABC'],
  y: [0.533, 9.7, 14.3, 15.7, 16.4, 23.4, 31.8, 51.20, 91, 155, 449, 11700],
  type: 'bar',
  name: 'CA',
  legendgroup: 'other',
  marker: {
    color: 'rgb(189,215,231)',
    opacity: 1.0,
  }
};
var traceFEE = {
  x: ['Default', 'SHREC', 'Loudun 1', 'Empire', 'Lans', 'Church', 'Pisa Cathedral', 'Euler', 'Munich', 'Train st.', 'Loudun 35', 'ABC'],
  y: [4.41,      41.47,    90.88,     175.16,   226.62, 353.97, 363.247, 802.647, 1593.529, 3044.943, 5425.90,   64200],
  type: 'bar',
  name: 'FEE',
  legendgroup: 'other',
  marker: {
    color: 'rgb(107,174,214)',
    opacity: 1.0,
  }
};
var tracePCPNet = {
  x: ['Default', 'SHREC', 'Loudun 1', 'Empire', 'Lans', 'Church', 'Pisa Cathedral', 'ABC'],
  y: [22.1,      354.97,  2100,       3262.67,  3608.33, 6400,    10600,            604800],
  type: 'bar',
  name: 'PCPNet',
  legendgroup: 'other',
  marker: {
    color: 'rgb(33,113,181)',
    opacity: 1.0,
  }
};
var traceEC = {
  x: ['Default', 'SHREC', 'Empire', 'Lans', 'ABC'],
  y: [2.09,       7.2,    343.19,    373.33, 1800000],
  type: 'bar',
  name: 'ECNet',
  legendgroup: 'other',
  marker: {
    color: '#002E63',
    opacity: 1.0,
  }
};
var traceGLS = {
  x: ['Default', 'SHREC', 'Loudun 1', 'Empire', 'Lans', 'Church', 'Pisa Cathedral', 'Euler', 'Munich', 'Train st.', 'Loudun 35', 'ABC'],
  y: [1.08,      14,      19.3,       36.4,     21,     58.4,     53.6,              115.2,  119.2,    331.9,       592.6,       9300],
  type: 'bar',
  name: 'GLS Precomputation',
  legendgroup: 'GLS-based',
  marker: {
    color: 'rgb(253,174,107)',
    opacity: 1.0,
  }
};
var tracePCED = {
  x: ['Default', 'SHREC', 'Loudun 1', 'Empire', 'Lans', 'Church', 'Pisa Cathedral', 'Euler', 'Munich', 'Train st.', 'Loudun 35', 'ABC'],
  y: [0.254,     3.1,     2.1,         2.1,      2.1,    3.4,     4.7,              7.1,      11.6,     25.7,       69.8,        1530],
  type: 'bar',
  name: 'GLS+PCED (ours)',
  legendgroup: 'GLS-based',
  marker: {
    color: 'rgb(35,139,69)',
    opacity: 1.0,
  }
};
var traceCNN = {
  x: ['Default', 'SHREC', 'Loudun 1', 'Empire', 'Lans', 'Church', 'Pisa Cathedral', 'Euler', 'Munich', 'Train st.', 'Loudun 35', 'ABC'],
  y: [2.03,      28.58,    54.39,     53.38,    55.06,   86.19,   117.26,           180.32,   281.84,   557.92,     1598.33,      5100],
  type: 'bar',
  name: 'GLS+CNN',
  legendgroup: 'GLS-based',
  marker: {
    color: 'rgb(186,228,179)',
    opacity: 1.0,
  }
};
var traceFC = {
  x: ['Default', 'SHREC', 'Loudun 1', 'Empire', 'Lans', 'Church', 'Pisa Cathedral', 'Euler', 'Munich', 'Train st.', 'Loudun 35', 'ABC'],
  y: [0.302,      3.1,    1.8,        1.8,      1.8,     2.9,      3.9,             6,       9.9,       19,          66.5,       1540],
  type: 'bar',
  name: 'GLS+FC',
  legendgroup: 'GLS-based',
  marker: {
    color: 'rgb(116,196,118)',
    opacity: 1.0,
  }
};

function addvector(a,b){
    return a.map((e,i) => e + b[i]);
}

tracePCED.y = addvector(tracePCED.y,traceGLS.y)
traceCNN.y  = addvector(traceCNN.y,traceGLS.y)
traceFC.y   = addvector(traceFC.y,traceGLS.y)

var data = [ traceCA,
             traceFEE,
             tracePCPNet,
             traceEC,
             traceGLS,
             traceCNN,
             traceFC,
             tracePCED,
           ];

var layout = {
  title: 'Classification time of the compared approaches - log scale (Figure 12 in paper)',
  xaxis: {
    tickangle: -45,
    tickson: "boundaries",
    ticklen: 15,
    showdividers: true,
    dividercolor: 'grey',
    dividerwidth: 2,
    tickfont: {
      size: 14
    }
  },
  yaxis: {
    type: 'log',
    autorange: true,
    tickfont: {
      size: 14
    }
  },
  barmode: 'group',
  font: {
    size: 14
  }
};

Plotly.newPlot('plot-timings', data, layout, {responsive: true});
});

