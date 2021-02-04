
function numberFormat(x) {
    var parts = x.toString().split(".");
    parts[0] = parts[0].replace(/\B(?=(\d{3})+(?!\d))/g, ",");
    return parts.join(".");
}

function ohlc_chart(chartDiv) {

    var market = document.getElementById("market");
    var base = document.getElementById("base");
    var quote = document.getElementById("quote");
    var datapoints = document.getElementById("datapoints");
    var candle = document.getElementById("candle");
    var candle_rate = document.getElementById("candle_rate");
    let apiSecret = document.getElementById("APISecret").value;

    // Themes begin
    am4core.useTheme(am4themes_dark);
    // am4core.useTheme(am4themes_animated);
    // Themes end

    var chart = am4core.create(chartDiv, am4charts.XYChart);
    chart.padding(15, 15, 15, 15);

    chart.dateFormatter.inputDateFormat = "yyyy-MM-dd HH:mm:ss";
    chart.leftAxesContainer.layout = "vertical";

    chart.dataSource.url = '/api/charts/ohlc/' + market.innerHTML + '/' + base.innerHTML + '/' + quote.innerHTML + '/' + datapoints.innerHTML + '/' + candle.innerHTML + '/' + apiSecret + '/';
    chart.dataSource.load();
    chart.dataSource.keepCount = true;
    chart.dataSource.parser = new am4core.JSONParser();
    chart.dataSource.updateCurrentData = true;
    chart.dataSource.reloadFrequency = parseInt(candle_rate.innerHTML) * 1000;


    
    

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
    ///dateAxis.groupData = true;


    dateAxis.start = 0.8;
    dateAxis.end = 1;
    dateAxis.keepSelection = true;


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

    // moving average BLUE

    var series_ma = chart.series.push(new am4charts.LineSeries());
    series_ma.dataFields.valueY = "moving_avg";
    series_ma.dataFields.dateX = "closetime";
    series_ma.strokeWidth = 1;
    series_ma.stroke = am4core.color("#002aff");

    /////////////

    // moving average exp YELLOW

    var series_ma = chart.series.push(new am4charts.LineSeries());
    series_ma.dataFields.valueY = "moving_exp";
    series_ma.dataFields.dateX = "closetime";
    series_ma.strokeWidth = 1;
    series_ma.stroke = am4core.color("#ffc400");

    /////////////


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

    valueAxis2.renderer.gridContainer.background.fill = am4core.color("#000000");
    valueAxis2.renderer.gridContainer.background.fillOpacity = 0.05;

    var series2 = chart.series.push(new am4charts.ColumnSeries());
    series2.dataFields.dateX = "closetime";
    series2.clustered = false;
    series2.dataFields.valueY = "volume";
    series2.yAxis = valueAxis2;
    series2.tooltipText = "{valueY.value}";
    series2.fillOpacity = 0.2;
    // volume should be summed
    ///series2.groupFields.valueY = "sum";


    chart.cursor = new am4charts.XYCursor();
    chart.cursor.behavior = "panX";
    chart.cursor.maxPanOut = 0.005
    // Create scrollbars
    chart.scrollbarX = new am4core.Scrollbar();

}

// NOT IN USE //
function latest_transactions() {
    let latestTransactions = document.getElementById('latest-transactions')
    fetch('/api/charts/ohlc/latest/' + document.getElementById("market").value + '/' + document.getElementById("pair").value + '/').then(function (response) {
        response.json().then(function (data) {
            linesHTML = '<div class="text-light text-center mb-2 small">Latest Transactions</div><div class="row text-light small"><div class="col text-right">Price</div><div class="col text-left">Amount</div></div>'
            for (let line of data.lines) {
                linesHTML += '<div class="row text-secondary small"><div class="col text-right">' + numberFormat(line['Price']) + '</div><div class="col text-left">' + numberFormat(line['Amount']) + '</div></div>'
            }
            latestTransactions.innerHTML = linesHTML
        })
    })
}

// NOT IN USE //
function getNewPrice() {
    fetch('/api/charts/ohlc/last-price/' + document.getElementById("market").value + '/' + document.getElementById("pair").value + '/').then(function (response) {
        response.json().then(function (data) {
            document.getElementById('last-price').innerHTML = numberFormat(data['price'])
        })
    })
}

// NOT IN USE //
function getNewAsks() {
    let asks = document.getElementById('asks')
    fetch('/api/charts/ohlc/new-asks/' + document.getElementById("market").value + '/' + document.getElementById("pair").value + '/').then(function (response) {
        response.json().then(function (data) {
            asksHTML = '<div class="text-light text-center mb-2 small">Order Book</div><div class="row small"><div class="col text-light text-right">Price</div><div class="col text-light text-left">Amount</div></div>'
            for (let askLine of data) {
                asksHTML += '<div class="row small"><div class="col text-danger text-right">' + numberFormat(askLine['price']) + '</div><div class="col text-danger text-left">' + numberFormat(askLine['amount']) + '</div></div>'
            }
            asks.innerHTML = asksHTML
        })
    })
}

// NOT IN USE //
function getNewBids() {
    let bids = document.getElementById('bids')
    fetch('/api/charts/ohlc/new-bids/' + document.getElementById("market").value + '/' + document.getElementById("pair").value + '/').then(function (response) {
        response.json().then(function (data) {
            bidsHTML = ''
            for (let bidLine of data) {
                bidsHTML += '<div class="row small"><div class="col text-success text-right">' + numberFormat(bidLine['price']) + '</div><div class="col text-success text-left">' + numberFormat(bidLine['amount']) + '</div></div>'
            }
            bids.innerHTML = bidsHTML
        })
    })
}

// NOT IN USE //
function orderBook() {
    // Themes begin
    am4core.useTheme(am4themes_dark);
    // am4core.useTheme(am4themes_animated);
    // Themes end

    // Create chart instance
    var chart = am4core.create("orderBook-chart", am4charts.XYChart);

    // Add data
    // '/api/charts/live/order-book/kraken/btcusd/'
    chart.dataSource.url = '/api/charts/live/order-book/' + document.getElementById("market").value + '/' + document.getElementById("pair").value + '/';
    chart.dataSource.reloadFrequency = 5.4*1000;
    chart.dataSource.adapter.add("parsedData", function (data) {

        // Function to process (sort and calculate cummulative volume)
        function processData(list, type, desc) {

            // Convert to data points
            for (var i = 0; i < list.length; i++) {
                list[i] = {
                    value: Number(list[i][0]),
                    volume: Number(list[i][1]),
                }
            }

            // Sort list just in case
            list.sort(function (a, b) {
                if (a.value > b.value) {
                    return 1;
                }
                else if (a.value < b.value) {
                    return -1;
                }
                else {
                    return 0;
                }
            });

            // Calculate cummulative volume
            if (desc) {
                for (var i = list.length - 1; i >= 0; i--) {
                    if (i < (list.length - 1)) {
                        list[i].totalvolume = list[i + 1].totalvolume + list[i].volume;
                    }
                    else {
                        list[i].totalvolume = list[i].volume;
                    }
                    var dp = {};
                    dp["value"] = list[i].value;
                    dp[type + "volume"] = list[i].volume;
                    dp[type + "totalvolume"] = list[i].totalvolume;
                    res.unshift(dp);
                }
            }
            else {
                for (var i = 0; i < list.length; i++) {
                    if (i > 0) {
                        list[i].totalvolume = list[i - 1].totalvolume + list[i].volume;
                    }
                    else {
                        list[i].totalvolume = list[i].volume;
                    }
                    var dp = {};
                    dp["value"] = list[i].value;
                    dp[type + "volume"] = list[i].volume;
                    dp[type + "totalvolume"] = list[i].totalvolume;
                    res.push(dp);
                }
            }

        }

        // Init
        var res = [];
        processData(data.bids, "bids", true);
        processData(data.asks, "asks", false);

        return res;
    });

    // Create axes
    var yAxis = chart.yAxes.push(new am4charts.CategoryAxis());
    yAxis.dataFields.category = "value";
    yAxis.renderer.opposite = true;
    yAxis.tooltip.disabled = true;
    yAxis.renderer.grid.template.disabled = true;
    yAxis.renderer.labels.template.disabled = true
    

    var xAxis = chart.xAxes.push(new am4charts.ValueAxis());
    xAxis.renderer.inversed = true;
    xAxis.tooltip.disabled = true;
    xAxis.renderer.grid.template.disabled = true;
    xAxis.renderer.labels.template.disabled = true

    // Create series
    var series = chart.series.push(new am4charts.StepLineSeries());
    series.dataFields.categoryY = "value";
    series.dataFields.valueX = "bidstotalvolume";
    series.strokeWidth = 2;
    series.stroke = am4core.color("#0f0");
    series.fill = series.stroke;
    series.fillOpacity = 0.1;
    series.tooltipText = "Bid: [bold]{categoryY}[/]\nVolume: [bold]{valueX}[/]"

    var series2 = chart.series.push(new am4charts.StepLineSeries());
    series2.dataFields.categoryY = "value";
    series2.dataFields.valueX = "askstotalvolume";
    series2.strokeWidth = 2;
    series2.stroke = am4core.color("#f00");
    series2.fill = series2.stroke;
    series2.fillOpacity = 0.1;
    series2.tooltipText = "Ask: [bold]{categoryY}[/]\nVolume: [bold]{valueX}[/]"


    // Add cursor
    chart.cursor = new am4charts.XYCursor();
}