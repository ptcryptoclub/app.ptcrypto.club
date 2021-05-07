function historical_line_pro(divName) {

    var candle_pro = document.getElementById("candle-pro").value;

    var start = document.getElementById("start-pro").value;
    var startTime = document.getElementById("start-time-pro").value;
    var end = document.getElementById("end-pro").value;
    var endTime = document.getElementById("end-time-pro").value;

    var base = document.getElementById("base-pro").value;
    var quote = document.getElementById("quote-pro").value;
    var market = document.getElementById("market-pro").value;
    var apiSecret = document.getElementById("APISecret").value;

    if (startTime != "") {
        start += " " + startTime
    }

    if (endTime != "") {
        end += " " + endTime
    }


    if (start == "" & end == "") {
        urlToSend = "/api/historical-charts/line/" + base + "/" + quote + "/" + market + "/" + candle_pro + "/" + apiSecret +"/"
    } else if (start != "" & end == "") {
        urlToSend = "/api/historical-charts/line/" + base + "/" + quote + "/" + market + "/" + candle_pro + "/" + apiSecret +"/?start="+ start;
    }else if (end != "" & start == "") {
        urlToSend = "/api/historical-charts/line/" + base + "/" + quote + "/" + market + "/" + candle_pro + "/" + apiSecret +"/?end="+ end;
    } else {
        urlToSend = "/api/historical-charts/line/" + base + "/" + quote + "/" + market + "/" + candle_pro + "/" + apiSecret +"/?start="+ start +"&end=" + end;
    }

    // Themes begin
    am4core.useTheme(am4themes_dark);
    am4core.useTheme(am4themes_animated);
    // Themes end

    // Auto dispose charts
    am4core.options.autoDispose = true;

    // Create chart
    var chart = am4core.create(divName, am4charts.XYChart);
    chart.padding(0, 15, 0, 15);
    chart.dateFormatter.inputDateFormat = "yyyy-MM-dd HH:mm:ss";

    // Load external data
    chart.dataSource.url = urlToSend;
    chart.dataSource.parser = new am4core.JSONParser();

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
    dateAxis.renderer.fontSize = "0.8em";

    // this makes the data to be grouped
    dateAxis.groupData = true;
    dateAxis.groupCount = 2000;


    var valueAxis = chart.yAxes.push(new am4charts.ValueAxis());
    valueAxis.tooltip.disabled = true;
    valueAxis.zIndex = 1;
    valueAxis.renderer.baseGrid.disabled = true;
    // valueAxis.title.text = base.innerHTML.toUpperCase() + quote.innerHTML.toUpperCase();
    valueAxis.title.fontSize = "0.8em"
    valueAxis.renderer.gridContainer.background.fill = am4core.color("#000000");
    valueAxis.renderer.gridContainer.background.fillOpacity = 0.05;
    valueAxis.renderer.inside = true;
    valueAxis.renderer.labels.template.verticalCenter = "bottom";
    valueAxis.renderer.labels.template.padding(2, 2, 2, 2);
    valueAxis.renderer.grid.template.disabled = true;

    valueAxis.renderer.fontSize = "0.8em"

    var series = chart.series.push(new am4charts.LineSeries());
    series.dataFields.dateX = "date";
    series.dataFields.valueY = "closeprice";
    series.tooltipText = "{valueY.value}";
    series.defaultState.transitionDuration = 0;
    series.fillOpacity = 0.2;

    chart.cursor = new am4charts.XYCursor();
}



function historical_ohlc_pro(divName) {
    
    var candle_pro = document.getElementById("candle-pro").value;

    var start = document.getElementById("start-pro").value;
    var startTime = document.getElementById("start-time-pro").value;
    var end = document.getElementById("end-pro").value;
    var endTime = document.getElementById("end-time-pro").value;

    var base = document.getElementById("base-pro").value;
    var quote = document.getElementById("quote-pro").value;
    var market = document.getElementById("market-pro").value;
    var apiSecret = document.getElementById("APISecret").value;

    if (startTime != "") {
        start += " " + startTime
    }

    if (endTime != "") {
        end += " " + endTime
    }


    if (start == "" & end == "") {
        urlToSend = "/api/historical-charts/ohlc/" + base + "/" + quote + "/" + market + "/" + candle_pro + "/" + apiSecret +"/"
    } else if (start != "" & end == "") {
        urlToSend = "/api/historical-charts/ohlc/" + base + "/" + quote + "/" + market + "/" + candle_pro + "/" + apiSecret +"/?start="+ start;
    }else if (end != "" & start == "") {
        urlToSend = "/api/historical-charts/ohlc/" + base + "/" + quote + "/" + market + "/" + candle_pro + "/" + apiSecret +"/?end="+ end;
    } else {
        urlToSend = "/api/historical-charts/ohlc/" + base + "/" + quote + "/" + market + "/" + candle_pro + "/" + apiSecret +"/?start="+ start +"&end=" + end;
    }

    // Themes begin
    am4core.useTheme(am4themes_dark);
    am4core.useTheme(am4themes_animated);
    // Themes end

    var chart = am4core.create(divName, am4charts.XYChart);
    chart.padding(15, 15, 15, 15);
    // Auto dispose charts
    am4core.options.autoDispose = true;

    chart.dateFormatter.inputDateFormat = "yyyy-MM-dd HH:mm:ss";
    chart.leftAxesContainer.layout = "vertical";
    // chart.zoomOutButton.disabled = true;

    chart.dataSource.url = urlToSend;
    chart.dataSource.parser = new am4core.JSONParser();

    var dateAxis = chart.xAxes.push(new am4charts.DateAxis());
    dateAxis.renderer.grid.template.location = 0;
    dateAxis.renderer.ticks.template.length = 8;
    dateAxis.renderer.ticks.template.strokeOpacity = 0.1;
    dateAxis.renderer.grid.template.disabled = true;
    dateAxis.renderer.ticks.template.disabled = false;
    dateAxis.renderer.ticks.template.strokeOpacity = 0.2;
    dateAxis.renderer.minLabelPosition = 0.01;
    dateAxis.renderer.maxLabelPosition = 0.99;
    dateAxis.minHeight = 30;
    dateAxis.renderer.fontSize = "0.8em"
    dateAxis.groupData = true;

    // dateAxis.minZoomCount = 120;

    var valueAxis = chart.yAxes.push(new am4charts.ValueAxis());
    valueAxis.tooltip.disabled = true;
    valueAxis.zIndex = 1;
    valueAxis.renderer.baseGrid.disabled = true;
    // height of axis
    valueAxis.height = am4core.percent(80);

    valueAxis.renderer.gridContainer.background.fill = am4core.color("#000000");
    valueAxis.renderer.gridContainer.background.fillOpacity = 0.05;
    valueAxis.renderer.inside = true;
    valueAxis.renderer.labels.template.verticalCenter = "bottom";
    valueAxis.renderer.labels.template.padding(2, 2, 2, 2);

    valueAxis.renderer.maxLabelPosition = 0.95;
    valueAxis.renderer.fontSize = "0.8em";
    valueAxis.renderer.grid.template.disabled = true;

    var series = chart.series.push(new am4charts.CandlestickSeries());
    series.dataFields.dateX = "closetime";
    series.dataFields.valueY = "closeprice";
    series.dataFields.openValueY = "openprice";
    series.dataFields.lowValueY = "lowprice";
    series.dataFields.highValueY = "highprice";
    series.tooltipText = "Open:{openValueY.value}\nHigh:{highValueY.value}\nLow:{lowValueY.value}\nClose:{valueY.value}";

    // important!
    // candlestick series colors are set in states.
    series.riseFromOpenState.properties.fill = am4core.color("#00ff00");
    series.dropFromOpenState.properties.fill = am4core.color("#FF0000");
    series.riseFromOpenState.properties.stroke = am4core.color("#00ff00");
    series.dropFromOpenState.properties.stroke = am4core.color("#FF0000");

    series.riseFromPreviousState.properties.fillOpacity = 1;
    series.dropFromPreviousState.properties.fillOpacity = 0;


    var valueAxis2 = chart.yAxes.push(new am4charts.ValueAxis());
    valueAxis2.tooltip.disabled = true;
    // height of axis
    valueAxis2.height = am4core.percent(20);
    valueAxis2.zIndex = 3;
    // this makes gap between panels
    // valueAxis2.marginTop = 30;
    valueAxis2.renderer.baseGrid.disabled = true;
    valueAxis2.renderer.inside = false;
    valueAxis2.renderer.labels.template.verticalCenter = "bottom";
    valueAxis2.renderer.labels.template.padding(2, 2, 2, 2);
    valueAxis2.renderer.maxLabelPosition = 0.95;
    valueAxis2.renderer.fontSize = "0.8em";

    valueAxis2.renderer.grid.template.disabled = true;

    var series2 = chart.series.push(new am4charts.ColumnSeries());
    series2.dataFields.dateX = "closetime";
    series2.clustered = false;
    series2.dataFields.valueY = "volume";
    series2.yAxis = valueAxis2;
    series2.tooltipText = "{valueY.value}";
    series2.fillOpacity = 0.2;
    // volume should be summed
    series2.groupFields.valueY = "sum";


    chart.cursor = new am4charts.XYCursor();
    // chart.cursor.behavior = "panX";
    chart.cursor.maxPanOut = 0.005
    // Create scrollbars
    chart.scrollbarX = new am4core.Scrollbar();
}



function historical_vtp_pro(divName) {
    
    var candle_pro = document.getElementById("candle-pro").value;

    var start = document.getElementById("start-pro").value;
    var startTime = document.getElementById("start-time-pro").value;
    var end = document.getElementById("end-pro").value;
    var endTime = document.getElementById("end-time-pro").value;

    var base = document.getElementById("base-pro").value;
    var quote = document.getElementById("quote-pro").value;
    var market = document.getElementById("market-pro").value;
    var apiSecret = document.getElementById("APISecret").value;

    if (startTime != "") {
        start += " " + startTime
    }

    if (endTime != "") {
        end += " " + endTime
    }


    if (start == "" & end == "") {
        urlToSend = "/api/historical-charts/vtp/" + base + "/" + quote + "/" + market + "/" + candle_pro + "/" + apiSecret +"/"
    } else if (start != "" & end == "") {
        urlToSend = "/api/historical-charts/vtp/" + base + "/" + quote + "/" + market + "/" + candle_pro + "/" + apiSecret +"/?start="+ start;
    }else if (end != "" & start == "") {
        urlToSend = "/api/historical-charts/vtp/" + base + "/" + quote + "/" + market + "/" + candle_pro + "/" + apiSecret +"/?end="+ end;
    } else {
        urlToSend = "/api/historical-charts/vtp/" + base + "/" + quote + "/" + market + "/" + candle_pro + "/" + apiSecret +"/?start="+ start +"&end=" + end;
    }

    // Themes begin
    am4core.useTheme(am4themes_dark);
    am4core.useTheme(am4themes_animated);
    // Themes end

    var chart = am4core.create(divName, am4charts.XYChart);
    // Auto dispose charts
    am4core.options.autoDispose = true;

    chart.dateFormatter.inputDateFormat = "yyyy-MM-dd HH:mm:ss";
    chart.leftAxesContainer.layout = "vertical";

    chart.dataSource.url = urlToSend;
    chart.dataSource.parser = new am4core.JSONParser();

    var dateAxis = chart.xAxes.push(new am4charts.DateAxis());
    dateAxis.renderer.grid.template.location = 0;
    dateAxis.renderer.fontSize = "0.8em"
    dateAxis.hidden = true;
    dateAxis.renderer.inside = true;
    dateAxis.tooltip.disabled = true;
    // dateAxis.start = 0.8;
    // dateAxis.end = 1;
    // dateAxis.keepSelection = true;
    dateAxis.renderer.grid.template.disabled = true;

    var dateAxis2 = chart.xAxes.push(new am4charts.DateAxis());
    dateAxis2.renderer.grid.template.location = 0;
    dateAxis2.renderer.fontSize = "0.8em"
    // dateAxis2.start = 0.8;
    // dateAxis2.end = 1;
    // dateAxis2.keepSelection = true;
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
    // chart.cursor.behavior = "panX";
    chart.cursor.maxPanOut = 0.005
    // Create scrollbars
    chart.scrollbarX = new am4core.Scrollbar();
}

