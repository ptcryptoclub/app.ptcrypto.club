

function lineChartFiat (divName, fiat) {

    let apiSecret = document.getElementById("APISecret").value;
    let delta = 24 // This will give us the last 24h

    // Themes begin
    am4core.useTheme(am4themes_dark);
    am4core.useTheme(am4themes_animated);
    // Themes end
    
    var chart = am4core.create(divName, am4charts.XYChart);
    chart.hiddenState.properties.opacity = 0;
    
    chart.padding(0, 0, 0, 0);
    
    chart.zoomOutButton.disabled = true;
    chart.dateFormatter.inputDateFormat = "yyyy-MM-dd HH:mm:ss";
    chart.dataSource.url = '/api/charts/fiat/line/'+ fiat +'/'+ delta +'/'+ apiSecret +'/'
    chart.dataSource.load();
    chart.dataSource.parser = new am4core.JSONParser();

    chart.cursor = new am4charts.XYCursor();
    chart.cursor.behavior = "none";
    
    var dateAxis = chart.xAxes.push(new am4charts.DateAxis());
    dateAxis.renderer.fontSize = "0.75em";
    dateAxis.tooltip.disabled = true;
    dateAxis.renderer.grid.template.disabled = true;
    

    var valueAxis = chart.yAxes.push(new am4charts.ValueAxis());
    valueAxis.tooltip.disabled = true;
    valueAxis.renderer.inside = true;
    valueAxis.renderer.minLabelPosition = 0.05;
    valueAxis.renderer.maxLabelPosition = 0.95;
    valueAxis.renderer.axisFills.template.disabled = true;
    valueAxis.renderer.ticks.template.disabled = true;
    valueAxis.renderer.fontSize = "0.75em"
    valueAxis.renderer.grid.template.disabled = true;
    valueAxis.title.text = fiat.toUpperCase();
    valueAxis.title.fontSize = "0.75em"
    
    var series = chart.series.push(new am4charts.LineSeries());
    series.dataFields.dateX = "date";
    series.dataFields.valueY = "price";
    series.tooltipText = "1 EUR = {valueY.value} "+fiat.toUpperCase();
    series.fillOpacity = 0.2;
    
    
    // add data
    var intervalFiatChartLine;
    function startInterval() {
        intervalFiatChartLine = setInterval(function() {
            fetch('/api/charts/fiat/line/'+ fiat +'/1/'+ apiSecret +'/').then(
                function(response){
                    response.json().then(
                        function (dataNew) {
                            var toAdd = { date: dataNew['date'], price: dataNew['price'] }
                            chart.addData(toAdd, 1);
                        }
                    )
                }
            );
        }, 3600 * 1000);
    }
    
    startInterval();
    
        
}
