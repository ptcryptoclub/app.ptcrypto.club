

function vtp_chart (divNane) {

    var market = document.getElementById("market");
    var base = document.getElementById("base");
    var quote = document.getElementById("quote");
    var datapoints = document.getElementById("datapoints");
    var candle = document.getElementById("candle");
    var candle_rate = document.getElementById("candle_rate");
    let apiSecret = document.getElementById("APISecret").value;

    // Themes begin
    am4core.useTheme(am4themes_dark);
    am4core.useTheme(am4themes_animated);
    // Themes end

    var chart = am4core.create(divNane, am4charts.XYChart);

    chart.dateFormatter.inputDateFormat = "yyyy-MM-dd HH:mm:ss";
    chart.leftAxesContainer.layout = "vertical";
    chart.zoomOutButton.disabled = true;

    chart.dataSource.url = '/api/charts/vtp/' + market.innerHTML + '/' + base.innerHTML + '/' + quote.innerHTML + '/' + datapoints.innerHTML + '/' + candle.innerHTML + '/' + apiSecret + '/';
    chart.dataSource.load();
    chart.dataSource.keepCount = true;
    chart.dataSource.parser = new am4core.JSONParser();
    chart.dataSource.updateCurrentData = true;
    chart.dataSource.reloadFrequency = parseInt(candle_rate.innerHTML) * 1000;

    var dateAxis = chart.xAxes.push(new am4charts.DateAxis());
    dateAxis.renderer.grid.template.location = 0;
    dateAxis.renderer.fontSize = "0.8em"
    dateAxis.hidden = true;
    dateAxis.renderer.inside = true;
    dateAxis.tooltip.disabled = true;
    dateAxis.start = 0.8;
    dateAxis.end = 1;
    dateAxis.keepSelection = true;
    dateAxis.renderer.grid.template.disabled = true;

    var dateAxis2 = chart.xAxes.push(new am4charts.DateAxis());
    dateAxis2.renderer.grid.template.location = 0;
    dateAxis2.renderer.fontSize = "0.8em"
    dateAxis2.start = 0.8;
    dateAxis2.end = 1;
    dateAxis2.keepSelection = true;
    dateAxis2.renderer.grid.template.disabled = true;

    var valueAxis = chart.yAxes.push(new am4charts.ValueAxis());
    valueAxis.tooltip.disabled = true;
    valueAxis.zIndex = 1;
    valueAxis.renderer.baseGrid.disabled = true;
    // height of axis
    valueAxis.height = am4core.percent(70);

    valueAxis.renderer.gridContainer.background.fill = am4core.color("#000000");
    valueAxis.renderer.gridContainer.background.fillOpacity = 0.05;
    valueAxis.renderer.inside = true;
    valueAxis.renderer.labels.template.verticalCenter = "bottom";
    valueAxis.renderer.labels.template.padding(2, 2, 2, 2);
    valueAxis.renderer.maxLabelPosition = 0.95;
    valueAxis.renderer.fontSize = "0.8em"
    valueAxis.renderer.grid.template.disabled = true;

    var valueAxis2 = chart.yAxes.push(new am4charts.ValueAxis());
    valueAxis2.tooltip.disabled = true;
    // height of axis
    valueAxis2.height = am4core.percent(20);
    valueAxis2.zIndex = 3
    // this makes gap between panels
    valueAxis2.marginTop = 5;
    valueAxis2.renderer.baseGrid.disabled = true;
    valueAxis2.renderer.inside = true;
    valueAxis2.renderer.labels.template.verticalCenter = "bottom";
    valueAxis2.renderer.labels.template.padding(2, 2, 2, 2);
    valueAxis2.renderer.maxLabelPosition = 0.95;
    valueAxis2.renderer.fontSize = "0.8em"
    valueAxis2.renderer.gridContainer.background.fill = am4core.color("#000000");
    valueAxis2.renderer.gridContainer.background.fillOpacity = 0.05;
    valueAxis2.renderer.grid.template.disabled = true;

    var valueAxis3 = chart.yAxes.push(new am4charts.ValueAxis());
    valueAxis3.tooltip.disabled = true;
    // height of axis
    valueAxis3.height = am4core.percent(10);
    valueAxis3.zIndex = 2
    // this makes gap between panels
    valueAxis3.marginTop = 5;
    valueAxis3.renderer.baseGrid.disabled = true;
    valueAxis3.renderer.inside = true;
    valueAxis3.renderer.labels.template.verticalCenter = "bottom";
    valueAxis3.renderer.labels.template.padding(2, 2, 2, 2);
    valueAxis3.renderer.maxLabelPosition = 0.95;
    valueAxis3.renderer.fontSize = "0.8em"
    valueAxis3.renderer.gridContainer.background.fill = am4core.color("#000000");
    valueAxis3.renderer.gridContainer.background.fillOpacity = 0.05;
    valueAxis3.renderer.grid.template.disabled = true;

    var series = chart.series.push(new am4charts.LineSeries());
    series.dataFields.dateX = "closetime";
    series.dataFields.valueY = "closeprice";
    series.tooltipText = "ClosePrice: {valueY.value}";
    series.tooltip.getFillFromObject = false;
    series.tooltip.background.fill = am4core.color("#0061e0");
    series.stroke = am4core.color("#0061e0");

    var series5 = chart.series.push(new am4charts.LineSeries());
    series5.dataFields.dateX = "closetime";
    series5.dataFields.valueY = "maxVolumePrice";
    series5.tooltipText = "PriceHV: {valueY.value}";
    series5.tooltip.getFillFromObject = false;
    series5.tooltip.background.fill = am4core.color("#e00000");
    series5.stroke = am4core.color("#e00000");

    var series2 = chart.series.push(new am4charts.ColumnSeries());
    series2.dataFields.dateX = "closetime";
    series2.dataFields.valueY = "volume";
    series2.stacked = true;
    series2.tooltipText = "RemVolume: {valueY.value}";
    series2.yAxis = valueAxis2;
    series2.tooltip.getFillFromObject = false;
    series2.tooltip.background.fill = am4core.color("#0061e0");
    series2.fill = am4core.color("#0061e0");
    series2.strokeWidth = 0;

    var series4 = chart.series.push(new am4charts.ColumnSeries());
    series4.dataFields.dateX = "closetime";
    series4.dataFields.valueY = "maxVolume";
    series4.stacked = true;
    series4.tooltipText = "HighestVolume: {valueY.value}";
    series4.yAxis = valueAxis2;
    series4.tooltip.getFillFromObject = false;
    series4.tooltip.background.fill = am4core.color("#e00000");
    series4.fill = am4core.color("#e00000");
    series4.strokeWidth = 0;

    var series3 = chart.series.push(new am4charts.ColumnSeries());
    series3.dataFields.dateX = "closetime";
    series3.dataFields.valueY = "nTrans";
    series3.tooltipText = "Transactions: {valueY.value}";
    series3.yAxis = valueAxis3;
    series3.xAxis = dateAxis2;
    series3.strokeWidth = 0;

    chart.cursor = new am4charts.XYCursor();
    chart.cursor.behavior = "panX";
    chart.cursor.maxPanOut = 0.005
    // Create scrollbars
    chart.scrollbarX = new am4core.Scrollbar();


}