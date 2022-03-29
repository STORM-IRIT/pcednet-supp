function getPRScatterPlot(precision, recall, markers)
{
    return  {
      x: recall,
      y: precision,
      mode: 'markers+text',
      type: 'scattergl',
      name: 'Median',
      textfont : {
        family:'Times New Roman'
      },
      textposition: 'left',
      text: dataset_properties['methods']['ShortNames'],
      hovertext: dataset_properties['methods']['Names'],
      marker: {
        size: 12,
        color: dataset_properties['methods']['NbClasses'],
        opacity: 0.4,
        colorscale: [
            [0, 'rgb(252,141,98)'],
            [0.5, 'rgb(252,141,98)'],

            [0.5, 'rgb(141,160,203)'],
            [1.0, 'rgb(141,160,203)']
        ],
        line: {
            color:'rgb(50,50,50)',
            width:1
        },
        type: 'heatmap',
        colorbar:{
          autotick: false,
          tick0: 0,
          dtick: 1,
          title: 'Nb Classes',
          margin: {t: 50},
          lenmode: "pixels",
          thickness : 30,
          len: 100,
          xanchor: "middle",
          yanchor: "top",
        },
        showscale: true,
        symbol: markers,
     }
    };
}

function getPRScatterLayout()
{
  return {
      xaxis: {
        range: [ 0, 1 ],
        title: 'Recall',
        linecolor: 'black',
        mirror: true,
      },
      yaxis: {
        range: [0, 1],
        title: 'Precision',
        linecolor: 'black',
        mirror: true,
      },
      margin: {
        t: 10,
      },
    };
}


function getHistogramLayout()
{
    return {
        title: 'Histograms',
        margin: { t: 30, },
        hoverlabel: { namelength : -1, },
        legend: {
            traceorder : 'grouped',
            orientation : 'h',
        },
        shapes: [
          {
          type: 'rect',
          xref: 'paper',
          yref: 'paper',
          x0: 0.9,
          y0: 0.3,
          x1: 1,
          y1: 1,
          line: {
            color: 'rgba(50, 200, 50, 0.2',
            width: 0
          },
          fillcolor: 'rgba(50, 200, 50, 0.2)',
          },
          {
          type: 'rect',
          xref: 'paper',
          yref: 'paper',
          x0: 0,
          y0: 0.3,
          x1: 0.25,
          y1: 1,
          line: {
            color: 'rgba(200, 50, 50, 0.2',
            width: 0
          },
          fillcolor: 'rgba(200, 50, 50, 0.2)',
          }
        ]
    };
}


function getPlotlyHistogramLayout()
{
    return {
        title: 'Histogram',
        barmode: "overlay",
        margin: { t: 30, },
        xaxis: {range: [-1, 1]},
        hoverlabel: { namelength : -1, },
        shapes: [
          {
          type: 'line',
          xref: 'paper',
          yref: 'paper',
          x0: 0.5,
          y0: 0,
          x1: 0.5,
          y1: 1,
          line: {
            width: 1
          }
          }
        ]
    };
}


function getPRPlotDataSingle(precision, recall)
{
    var trace1 = {
      x: recall,
      y: precision,
      mode: 'markers',
      name: 'points',
      marker: {
        color: 'rgb(102,0,0)',
        size: 2,
        opacity: 0.4
      },
      type: 'scatter'
    };
    var trace2 = {
      x: recall,
      y: precision,
      name: 'density',
      ncontours: 20,
      colorscale: 'Hot',
      reversescale: true,
      showscale: false,
      type: 'histogram2dcontour',
      contours: {
        start:50,
        end:1000,
      },
    };
    return [trace1, trace2];
}

function getPRLayoutSingle(title)
{
  return {
      title: title,
      showlegend: false,
      autosize: false,
      width: 500,
      height: 500,
      margin: {t: 100},
      hovermode: 'closest',
      bargap: 0,
      font: {
        size: 30
      },
      xaxis: {
        linecolor: 'black',
        mirror: true,
        tickfont: {
          size: 35
        },
        range: [0, 1.1]
      },
      yaxis: {
        linecolor: 'black',
        mirror: true,
        tickfont: {
          size: 30
        },
        range: [0, 1.1]
      },
    };
  }



function getPRPlotData2(precision1, recall1, precision2, recall2)
{
    var trace1 = {
      x: recall1,
      y: precision1,
      mode: 'markers',
      name: 'Precision/Recall (samples)',
      marker: {
        color: 'rgb(102,0,0)',
        size: 2,
        opacity: 0.4
      },
      type: 'scattergl'
    };
    var trace2 = {
      x: recall1,
      y: precision1,
      name: 'Precision/Recall (density)',
      bingroup : 1,
      coloraxis : "coloraxis",
      type: 'histogram2dcontour'
    };
    var trace3 = {
      x: recall1,
      name: 'Recall (density)',
      marker: {color: 'rgb(102,0,0)'},
      yaxis: 'y2',
      type: 'histogram',
      nbinsx: 100
    };
    var trace4 = {
      y: precision1,
      name: 'Precision (density)',
      marker: {color: 'rgb(102,0,0)'},
      xaxis: 'x2',
      type: 'histogram',
      nbinsx: 100,
    };
    var trace5 = {
      x: recall2,
      y: precision2,
      mode: 'markers',
      name: 'Precision/Recall (samples)',
      marker: {
        color: 'rgb(102,0,0)',
        size: 2,
        opacity: 0.4
      },
      xaxis: 'x3',
      type: 'scattergl'
    };
    var trace6 = {
      x: recall2,
      y: precision2,
      name: 'Precision/Recall (density)',
      bingroup : 1,
      coloraxis : "coloraxis",
      xaxis: 'x3',
      type: 'histogram2dcontour'
    };
    var trace7 = {
      x: recall2,
      name: 'Recall (density)',
      marker: {color: 'rgb(102,0,0)'},
      xaxis: 'x3',
      yaxis: 'y2',
      type: 'histogram',
      nbinsx: 100
    };
    var trace8 = {
      y: precision2,
      name: 'Precision (density)',
      marker: {color: 'rgb(102,0,0)'},
      xaxis: 'x4',
      type: 'histogram',
      nbinsx: 100,
    };
    return [trace1, trace2, trace3, trace4, trace5, trace6, trace7, trace8];
}

function getPRLayout2(title1, title2)
{
  return {
      showlegend: false,
      margin: {t: 50},
      hovermode: 'closest',
      bargap: 0,
      coloraxis: { // color axis shared between the density maps
        colorscale: 'Hot',
        reversescale: true,
        ncontours: 20,
      },
      xaxis: {
        domain: [0, 0.4],
        showgrid: false,
        zeroline: false,
        title: title1
      },
      yaxis: {
        domain: [0, 0.8],
        showgrid: false,
        zeroline: false
      },
      xaxis2: {
        domain: [0.4, 0.48],
        showgrid: false,
        zeroline: false
      },
      xaxis3: {
        domain: [0.5, 0.9],
        showgrid: false,
        zeroline: false,
        title: title2
      },
      xaxis4: {
        domain: [0.9, 0.98],
        showgrid: false,
        zeroline: false,
        matches:  'x2' //share the same interval
      },
      yaxis2: {
        domain: [0.8, 0.96],
        showgrid: false,
        nbinsx: false
      }
    };
  }

