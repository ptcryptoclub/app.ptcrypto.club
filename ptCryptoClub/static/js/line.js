function numberFormat(x) {
    var parts = x.toString().split(".");
    parts[0] = parts[0].replace(/\B(?=(\d{3})+(?!\d))/g, ",");
    return parts.join(".");
}


function update_values () {
    let borderLine = document.getElementById("general");
    let market = document.getElementById("market");
    let base = document.getElementById("base");
    let quote = document.getElementById("quote");
    let delta = document.getElementById("delta");
    let change = document.getElementById("change");
    let price = document.getElementById("last");
    let high = document.getElementById("high");
    let low = document.getElementById("low");
    let volume = document.getElementById("volume");
    let volumeQuote = document.getElementById("volumequote");
    let apiSecret = document.getElementById("APISecret").value;

    fetch('/api/line-chart/info/' + market.innerHTML + '/' + base.innerHTML + '/' + quote.innerHTML + '/' + delta.innerHTML + '/' + apiSecret + '/').then(
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
                    price.innerHTML = numberFormat(data['last_price']);
                    high.innerHTML = '<strong>High: </strong>' + numberFormat(data['high']);
                    low.innerHTML = '<strong>Low: </strong>' + numberFormat(data['low']);
                    volume.innerHTML = numberFormat(data['volume']) + ' ' + base.innerHTML.toUpperCase();
                    volumeQuote.innerHTML = numberFormat(data['volume_quote']) + ' ' + quote.innerHTML.toUpperCase();
                }
            )
        }
    );
}



function lineChart() {
    let market = document.getElementById("market");
    let base = document.getElementById("base");
    let quote = document.getElementById("quote");
    let last_x_hours = document.getElementById("last_x_hours");
    let apiSecret = document.getElementById("APISecret").value;

    // Themes begin
    am4core.useTheme(am4themes_dark);
    am4core.useTheme(am4themes_animated);
    // Themes end

    // Create chart
    var chart = am4core.create("line-chart", am4charts.XYChart);
    chart.padding(0, 15, 0, 15);
    chart.dateFormatter.inputDateFormat = "yyyy-MM-dd HH:mm:ss";

    // Load external data
    chart.dataSource.url = "/api/charts/line/" + market.innerHTML + '/' + base.innerHTML + '/' + quote.innerHTML + '/' + last_x_hours.innerHTML + '/' + apiSecret + '/';
    chart.dataSource.keepCount = true;
    chart.dataSource.parser = new am4core.JSONParser();
    chart.dataSource.reloadFrequency = 20 * 1000;
    chart.dataSource.updateCurrentData = true;

    // the following line makes value axes to be arranged vertically.
    chart.leftAxesContainer.layout = "vertical";

    // uncomment this line if you want to change order of axes
    //chart.bottomAxesContainer.reverseOrder = true;

    var dateAxis = chart.xAxes.push(new am4charts.DateAxis());
    dateAxis.renderer.grid.template.location = 0;
    dateAxis.renderer.ticks.template.length = 8;
    dateAxis.renderer.ticks.template.strokeOpacity = 0.1;
    dateAxis.renderer.grid.template.disabled = true;
    dateAxis.renderer.ticks.template.disabled = false;
    dateAxis.renderer.ticks.template.strokeOpacity = 0.2;
    dateAxis.renderer.minLabelPosition = 0.01;
    dateAxis.renderer.maxLabelPosition = 0.99;
    dateAxis.keepSelection = true;
    dateAxis.minHeight = 30;
    dateAxis.renderer.grid.template.disabled = true;



    var valueAxis = chart.yAxes.push(new am4charts.ValueAxis());
    valueAxis.tooltip.disabled = true;
    valueAxis.zIndex = 1;
    valueAxis.renderer.baseGrid.disabled = true;
    // height of axis
    valueAxis.height = am4core.percent(75);

    valueAxis.renderer.gridContainer.background.fill = am4core.color("#000000");
    valueAxis.renderer.gridContainer.background.fillOpacity = 0.05;
    valueAxis.renderer.inside = true;
    valueAxis.renderer.labels.template.verticalCenter = "bottom";
    valueAxis.renderer.labels.template.padding(2, 2, 2, 2);
    valueAxis.renderer.grid.template.disabled = true;

    //valueAxis.renderer.maxLabelPosition = 0.95;
    valueAxis.renderer.fontSize = "0.8em"

    var series = chart.series.push(new am4charts.LineSeries());
    series.dataFields.dateX = "date";
    series.dataFields.valueY = "closeValue";
    series.tooltipText = "{valueY.value}";
    series.defaultState.transitionDuration = 0;
    // series.stroke = "red"

    var valueAxis2 = chart.yAxes.push(new am4charts.ValueAxis());
    valueAxis2.tooltip.disabled = true;
    // height of axis
    valueAxis2.height = am4core.percent(25);
    valueAxis2.zIndex = 3
    // this makes gap between panels
    valueAxis2.marginTop = 30;
    valueAxis2.renderer.baseGrid.disabled = true;
    valueAxis2.renderer.inside = true;
    valueAxis2.renderer.labels.template.verticalCenter = "bottom";
    valueAxis2.renderer.labels.template.padding(2, 2, 2, 2);
    //valueAxis.renderer.maxLabelPosition = 0.95;
    valueAxis2.renderer.fontSize = "0.8em"
    valueAxis2.renderer.grid.template.disabled = true;

    valueAxis2.renderer.gridContainer.background.fill = am4core.color("#000000");
    valueAxis2.renderer.gridContainer.background.fillOpacity = 0.05;

    var series2 = chart.series.push(new am4charts.ColumnSeries());
    series2.dataFields.dateX = "date";
    series2.dataFields.valueY = "volume";
    series2.yAxis = valueAxis2;
    series2.tooltipText = "{valueY.value}";
    series2.defaultState.transitionDuration = 0;

    chart.cursor = new am4charts.XYCursor();

}