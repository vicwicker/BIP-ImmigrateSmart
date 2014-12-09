// This is a manifest file that'll be compiled into application.js, which will include all the files
// listed below.
//
// Any JavaScript/Coffee file within this directory, lib/assets/javascripts, vendor/assets/javascripts,
// or vendor/assets/javascripts of plugins, if any, can be referenced here using a relative path.
//
// It's not advisable to add code directly here, but if you do, it'll appear at the bottom of the
// the compiled file.
//
// WARNING: THE FIRST BLANK LINE MARKS THE END OF WHAT'S TO BE PROCESSED, ANY BLANK LINE SHOULD
// GO AFTER THE REQUIRES BELOW.
//
//= require jquery
//= require jquery_ujs
//= require_tree .
function drawChart(chartContainer,chartType,chartData,seriesName,chartTitle,subtitle,chartYaxis,chartXaxis){
        
    var piePOs= {pie:{    
                allowPointSelect: true,
                cursor: 'pointer',
                dataLabels: {
                    enabled: true,
                    format: '<b>{point.name}</b>: {point.y:.1f} %',
                    style: {
                        color: (Highcharts.theme && Highcharts.theme.contrastTextColor) || 'black'
                    }
                },
                showInLegend: true
        }};
    $(chartContainer).highcharts({
        chart: {

            type: chartType,
            plotBackgroundColor: null,
            plotBorderWidth: 1,//null,
            plotShadow: false
        },

        title: {
         text: chartTitle
        },
        subtitle: {
         text: subtitle
        },
        xAxis:{categories:chartXaxis},
        plotOptions: piePOs,
        tooltip: {
          pointFormat: '{series.name}: <b>{point.y:.1f}%</b>'
        },
        legend:{
            title:chartXaxis
        },
        series: [{
            type:chartType,
            name: seriesName,
            data: chartData
        }]
    });
}
