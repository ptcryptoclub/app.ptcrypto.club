function historical_line_prefix(divName, prefix) {

    var b1 = document.getElementById("start");
    var b2 = document.getElementById("start_time");
    var b3 = document.getElementById("end");
    var b4 = document.getElementById("end_time");

    if (b1 != null) {
        b1.value = ""
        b2.value = ""
        b3.value = ""
        b4.value = ""
    }

    

    var base = document.getElementById("base").value;
    var quote = document.getElementById("quote").value;
    var market = document.getElementById("market").value;
    var apiSecret = document.getElementById("APISecret").value;

    var a1 = document.getElementById("id1");
    var a2 = document.getElementById("id3");
    var a3 = document.getElementById("id7");
    var a4 = document.getElementById("id14");
    var a5 = document.getElementById("id30");

    a1.className = "btn btn-sm btn-outline-dark text-light px-2"
    a2.className = "btn btn-sm btn-outline-dark text-light px-2"
    a3.className = "btn btn-sm btn-outline-dark text-light px-2"
    a4.className = "btn btn-sm btn-outline-dark text-light px-2"
    a5.className = "btn btn-sm btn-outline-dark text-light px-2"

    elementID = "id" + prefix
    var prefixSelected = document.getElementById(elementID);
    prefixSelected.className = "btn btn-sm btn-secondary text-light px-2"

    var nowTime = new Date();

    var end_y = nowTime.getUTCFullYear()
    var end_m = parseInt(nowTime.getUTCMonth()) + 1
    var end_d = nowTime.getUTCDate()
    var end_h = nowTime.getUTCHours()
    var end_mm = nowTime.getUTCMinutes()
    var end_s = nowTime.getUTCSeconds()

    var end = end_y + "-" + end_m + "-" + end_d + " " + end_h + ":" + end_mm + ":" + end_s

    nowTime.setDate(nowTime.getDate()-prefix);

    var start_y = nowTime.getUTCFullYear()
    var start_m = parseInt(nowTime.getUTCMonth()) + 1
    var start_d = nowTime.getUTCDate()
    var start_h = nowTime.getUTCHours()
    var start_mm = nowTime.getUTCMinutes()
    var start_s = nowTime.getUTCSeconds()

    var start = start_y + "-" + start_m + "-" + start_d + " " + start_h + ":" + start_mm + ":" + start_s

    urlToSend = "/api/historical-charts/line/" + base + "/" + quote + "/" + market + "/300/" + apiSecret +"/?start="+ start +"&end=" + end;



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
