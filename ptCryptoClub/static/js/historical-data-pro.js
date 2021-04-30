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