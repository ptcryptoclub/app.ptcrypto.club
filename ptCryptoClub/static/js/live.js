
function liveChart() {
    // Themes begin
    am4core.useTheme(am4themes_dark);
    am4core.useTheme(am4themes_animated);
    // Themes end

    // Create chart instance
    var chart = am4core.create("live-chart", am4charts.XYChart);
    chart.dateFormatter.inputDateFormat = "yyyy-MM-dd HH:mm:ss";
    chart.legend = new am4charts.Legend();
    chart.legend.position = "top";

    // Add data
    chart.dataSource.url = '/api/charts/live/last-price/' + document.getElementById("market").innerHTML + '/' + document.getElementById("pair").innerHTML + '/'
    chart.dataSource.load();
    chart.dataSource.parser = new am4core.JSONParser();
    // chart.dataSource.keepCount = true;
    chart.dataSource.incremental = true;
    chart.dataSource.reloadFrequency = 5 * 1000;

    // Create axes
    var dateAxis = chart.xAxes.push(new am4charts.DateAxis());
    dateAxis.renderer.grid.template.disabled = true;


    var valueAxis = chart.yAxes.push(new am4charts.ValueAxis());
    valueAxis.tooltip.disabled = true;
    valueAxis.renderer.grid.template.disabled = true;

    // Create series
    var series = chart.series.push(new am4charts.LineSeries());
    series.dataFields.openValueY = "bid";
    series.dataFields.valueY = "ask";
    series.dataFields.dateX = "date";
    series.strokeWidth = 2;
    series.minBulletDistance = 10;
    series.tooltipText = "Ask: {valueY}\nBid: {openValueY}";
    series.tooltip.pointerOrientation = "vertical";
    series.tooltip.background.cornerRadius = 20;
    series.tooltip.background.fillOpacity = 0.5;
    series.tooltip.label.padding(12, 12, 12, 12)
    series.stroke = am4core.color("red")
    series.name = 'asks'
    series.tensionX = 0.8;


    // Add cursor
    chart.cursor = new am4charts.XYCursor();
    chart.cursor.lineY.opacity = 0;
    chart.cursor.xAxis = dateAxis;
    chart.cursor.snapToSeries = series;

    // Add bullet
    var bullet = series.createChild(am4charts.CircleBullet);
    bullet.circle.radius = 5;
    bullet.fillOpacity = 1;
    bullet.fill = am4core.color("red");
    bullet.isMeasured = false;

    series.events.on("validated", function () {
        bullet.moveTo(series.dataItems.last.point);
        bullet.validatePosition();
    });



    // Create series2
    var series2 = chart.series.push(new am4charts.LineSeries());
    series2.dataFields.valueY = "bid";
    series2.dataFields.dateX = "date";
    series2.strokeWidth = 2;
    series2.minBulletDistance = 10;
    series2.tooltipText = "{valueY}";
    series2.tooltip.pointerOrientation = "vertical";
    series2.tooltip.background.cornerRadius = 20;
    series2.tooltip.background.fillOpacity = 0.5;
    series2.tooltip.label.padding(12, 12, 12, 12)
    series2.stroke = am4core.color("green")
    series2.name = 'bids'
    series2.tensionX = 0.8;


    // Add bullet
    var bullet2 = series2.createChild(am4charts.CircleBullet);
    bullet2.circle.radius = 5;
    bullet2.fillOpacity = 1;
    bullet2.fill = am4core.color("green");
    bullet2.isMeasured = false;

    series2.events.on("validated", function () {
        bullet2.moveTo(series2.dataItems.last.point);
        bullet2.validatePosition();
    });


}

function numberFormat(x) {
    var parts = x.toString().split(".");
    parts[0] = parts[0].replace(/\B(?=(\d{3})+(?!\d))/g, ",");
    return parts.join(".");
}


function update_values () {
    let borderLine = document.getElementById("border-line");
    let pair = document.getElementById("pair");
    let market = document.getElementById("market");
    let change = document.getElementById("change");
    let price = document.getElementById("price");
    let high = document.getElementById("high");
    let low = document.getElementById("low");
    let volume = document.getElementById("volume");
    let volumeQuote = document.getElementById("volumeQuote");

    fetch('/api/line-chart/info/' + market.innerHTML + '/' + pair.innerHTML).then(
        function(response){
            response.json().then(
                function (data) {
                    change.innerHTML = data['change'] + '%';
                    if (data['change'] < 0) {
                        borderLine.className = 'p-4 my-4 border border-danger rounded-lg'
                        change.className = 'text-danger ml-3'
                        price.className = 'text-right text-danger'
                    } else if (data['change'] === 0) {
                        borderLine.className = 'p-4 my-4 border border-warning rounded-lg'
                        change.className = 'text-warning ml-3'
                        price.className = 'text-right text-warning'
                    } else {
                        borderLine.className = 'p-4 my-4 border border-success rounded-lg'
                        change.className = 'text-success ml-3'
                        price.className = 'text-right text-success'
                    }
                    price.innerHTML = numberFormat(data['last']);
                    high.innerHTML = '<strong>High: </strong>' + numberFormat(data['high']);
                    low.innerHTML = '<strong>Low: </strong>' + numberFormat(data['low']);
                    volume.innerHTML = numberFormat(data['volume']);
                    volumeQuote.innerHTML = numberFormat(data['volumeQuote']);
                    borderLine.hidden = false
                }
            )
        }
    );
}