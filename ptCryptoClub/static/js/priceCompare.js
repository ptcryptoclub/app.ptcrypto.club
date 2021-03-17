

function priceCompareChart (divName, market, base1, base2, quote, data_points) {

    let apiSecret = document.getElementById("APISecret").value;

    // Themes begin
    am4core.useTheme(am4themes_dark);
    am4core.useTheme(am4themes_animated);
    // Themes end
    
    var chart = am4core.create(divName, am4charts.XYChart);
    chart.hiddenState.properties.opacity = 0;
    
    chart.padding(0, 0, 0, 0);
    
    chart.zoomOutButton.disabled = true;
    chart.dateFormatter.inputDateFormat = "yyyy-MM-dd HH:mm:ss";

    chart.dataSource.url = '/api/price/'+ market +'/'+ base1 +'/'+ base2 +'/'+ quote +'/'+ data_points +'/'+ apiSecret +'/'
    chart.dataSource.load();
    chart.dataSource.parser = new am4core.JSONParser();

    chart.cursor = new am4charts.XYCursor();
    chart.cursor.behavior = "none";
    chart.legend = new am4charts.Legend();
    chart.legend.position = "top"
    
    var dateAxis = chart.xAxes.push(new am4charts.DateAxis());
    dateAxis.renderer.grid.template.location = 0;
    dateAxis.renderer.minGridDistance = 80;
    dateAxis.dateFormats.setKey("hour", "h:mm:ss");
    dateAxis.periodChangeDateFormats.setKey("second", "h:mm");
    dateAxis.periodChangeDateFormats.setKey("minute", "h:mm");
    dateAxis.periodChangeDateFormats.setKey("hour", "h:mm");
    //dateAxis.renderer.inside = true;
    dateAxis.renderer.axisFills.template.disabled = true;
    dateAxis.renderer.ticks.template.disabled = true;
    dateAxis.renderer.fontSize = "0.75em";
    dateAxis.renderer.grid.template.disabled = true;
    

    var valueAxis = chart.yAxes.push(new am4charts.ValueAxis());
    valueAxis.tooltip.disabled = true;
    valueAxis.interpolationDuration = 500;
    valueAxis.rangeChangeDuration = 500;
    valueAxis.renderer.inside = true;
    valueAxis.renderer.minLabelPosition = 0.05;
    valueAxis.renderer.maxLabelPosition = 0.95;
    valueAxis.renderer.axisFills.template.disabled = true;
    valueAxis.renderer.ticks.template.disabled = true;
    valueAxis.renderer.fontSize = "0.75em"
    valueAxis.title.text = base1.toUpperCase();
    valueAxis.title.fill = am4core.color("#f7931a");
    valueAxis.renderer.grid.template.disabled = true;

    var valueAxis2 = chart.yAxes.push(new am4charts.ValueAxis());
    valueAxis2.tooltip.disabled = true;
    valueAxis2.interpolationDuration = 500;
    valueAxis2.rangeChangeDuration = 500;
    valueAxis2.renderer.inside = true;
    valueAxis2.renderer.minLabelPosition = 0.05;
    valueAxis2.renderer.maxLabelPosition = 0.95;
    valueAxis2.renderer.axisFills.template.disabled = true;
    valueAxis2.renderer.ticks.template.disabled = true;
    valueAxis2.renderer.fontSize = "0.75em"
    valueAxis2.renderer.opposite = true;
    valueAxis2.title.text = base2.toUpperCase();
    valueAxis2.title.fill = am4core.color("#3aa7c8");
    valueAxis2.renderer.grid.template.disabled = true;
    
    var series = chart.series.push(new am4charts.LineSeries());
    series.dataFields.dateX = "date";
    series.dataFields.valueY = "price1";
    series.interpolationDuration = 500;
    series.defaultState.transitionDuration = 0;
    series.fill = am4core.color("#f7931a");
    series.stroke = am4core.color("#f7931a");
    series.tensionX = 0.8;
    series.tooltipText = base1.toUpperCase() + ": {valueY.value}";
    series.name = base1.toUpperCase()

    var series2 = chart.series.push(new am4charts.LineSeries());
    series2.dataFields.dateX = "date";
    series2.dataFields.valueY = "price2";
    series2.interpolationDuration = 500;
    series2.defaultState.transitionDuration = 0;
    series2.fill = am4core.color("#3aa7c8");
    series2.stroke = am4core.color("#3aa7c8");
    series2.tensionX = 0.8;
    series2.tooltipText = base2.toUpperCase() + ": {valueY.value}";
    series2.yAxis = valueAxis2;
    series2.name = base2.toUpperCase()


    //valueAxis.renderer.labels.template.fill = series.stroke;
    //valueAxis2.renderer.labels.template.fill = series2.stroke;

    
    chart.events.on("datavalidated", function () {
        dateAxis.zoom({ start: 1 / 15, end: 1.2 }, false, true);
    });
    
    dateAxis.interpolationDuration = 500;
    dateAxis.rangeChangeDuration = 500;
    
    
    // add data
    var interval;
    function startInterval() {
        interval = setInterval(function() {
            fetch('/api/price/'+ market +'/'+ base1 +'/'+ base2 +'/'+ quote +'/1/'+ apiSecret +'/').then(
                function(response){
                    response.json().then(
                        function (dataNew) {
                            var toAdd = { date: dataNew[0]['date'], price1: dataNew[0]['price1'], price2: dataNew[0]['price2'] }
                            chart.addData(toAdd, 1);
                        }
                    )
                }
            );
        }, 20 * 1000);
    }
    
    startInterval();
    
    // all the below is optional, makes some fancy effects
        
    // bullet at the front of the line
    var bullet = series.createChild(am4charts.CircleBullet);
    bullet.circle.radius = 5;
    bullet.fillOpacity = 1;
    bullet.fill = am4core.color("#f7931a");
    bullet.isMeasured = false;

    var bullet2 = series2.createChild(am4charts.CircleBullet);
    bullet2.circle.radius = 5;
    bullet2.fillOpacity = 1;
    bullet2.fill = am4core.color("#3aa7c8");
    bullet2.isMeasured = false;
    
    series.events.on("validated", function() {
        bullet.moveTo(series.dataItems.last.point);
        bullet.validatePosition();
    });

    series2.events.on("validated", function() {
        bullet2.moveTo(series2.dataItems.last.point);
        bullet2.validatePosition();
    });
        
}
