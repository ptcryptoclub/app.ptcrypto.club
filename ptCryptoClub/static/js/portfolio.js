

function buyReport() {
    let market = document.getElementById("market").value;
    let base = document.getElementById("base").value;
    let quote = document.getElementById("quote").value;
    fetch('/api/account/portfolio/price/' + market + '/' + base + '/' + quote + '/').then(
        function(response){
            response.json().then(
                function (data){
                    price = data['price']
                    amountSpent = document.getElementById("amount_spent").value
                    amountAsset = amountSpent/price

                    displayPrice = document.getElementById("price");
                    displayAmount = document.getElementById("amount");
                    displayResult = document.getElementById("result");

                    displayPrice.innerHTML = price + ' <small>' + quote.toUpperCase() + '</small>';
                    displayAmount.innerHTML = amountSpent + ' <small>' + quote.toUpperCase() + '</small>';
                    displayResult.innerHTML = amountAsset.toFixed(8) + ' <small>' + base.toUpperCase() + '</small>';
                }
            )
        }
    )
}


function updateBase() {
    let market = document.getElementById("market").value;
    let base_select = document.getElementById("base");
    fetch('/api/account/portfolio/dropdowns/base/' + market + '/').then(
        function(response){
            response.json().then(
                function (data){
                    let linesHTML = '';
                    for (let line of data) {
                        linesHTML += '<option value="' + line['base'] + '">' + line['base'].toUpperCase() + '</option>'
                    }
                    base_select.innerHTML = linesHTML
                }
            )
        }
    )
}


function updateQuote() {
    let market = document.getElementById("market").value;
    let base = document.getElementById("base").value;
    let quote_select = document.getElementById("quote");
    if (base === '') {

    } else {
        fetch('/api/account/portfolio/dropdowns/quote/' + market + '/' + base + '/').then(
            function(response){
                response.json().then(
                    function (data){
                        let linesHTML = '';
                        for (let line of data) {
                            linesHTML += '<option value="' + line['quote'] + '">' + line['quote'].toUpperCase() + '</option>'
                        }
                        quote_select.innerHTML = linesHTML
                    }
                )
            }
        )
    }
}


function pieWalletAssets(divName) {
    // Create chart instance
    var chart = am4core.create(divName, am4charts.PieChart);

    // Add data
    chart.data = [ {
      "type": "Wallet",
      "value": 501.9
    }, {
      "type": "Assets",
      "value": 301.9
    }];

    // Set inner radius
    chart.innerRadius = am4core.percent(50);

    // Add and configure Series
    var pieSeries = chart.series.push(new am4charts.PieSeries());
    pieSeries.dataFields.value = "value";
    pieSeries.dataFields.category = "type";
    pieSeries.slices.template.stroke = am4core.color("#fff");
    pieSeries.slices.template.strokeWidth = 2;
    pieSeries.slices.template.strokeOpacity = 1;

    // This creates initial animation
    pieSeries.hiddenState.properties.opacity = 1;
    pieSeries.hiddenState.properties.endAngle = -90;
    pieSeries.hiddenState.properties.startAngle = -90;
}


function pieAssets(divName) {
    // Create chart instance
    var chart = am4core.create(divName, am4charts.PieChart);

    // Add data
    chart.data = [ {
      "type": "BTC",
      "value": 10
    }, {
      "type": "ETH",
      "value": 30
    }];

    // Set inner radius
    chart.innerRadius = am4core.percent(50);

    // Add and configure Series
    var pieSeries = chart.series.push(new am4charts.PieSeries());
    pieSeries.dataFields.value = "value";
    pieSeries.dataFields.category = "type";
    pieSeries.slices.template.stroke = am4core.color("#fff");
    pieSeries.slices.template.strokeWidth = 2;
    pieSeries.slices.template.strokeOpacity = 1;

    // This creates initial animation
    pieSeries.hiddenState.properties.opacity = 1;
    pieSeries.hiddenState.properties.endAngle = -90;
    pieSeries.hiddenState.properties.startAngle = -90;
}


function lineBuySell(divName) {
    // Themes begin
    am4core.useTheme(am4themes_dark);
    am4core.useTheme(am4themes_animated);
    // Themes end

    // Create chart instance
    var chart = am4core.create(divName, am4charts.XYChart);

    chart.colors.step = 2;
    chart.maskBullets = false;

    // Add data
    chart.data = [{
        "date": "2012-01-01",
        "buy": 227,
        "sell": 135,
        "total_buy": 408,
        "total_sell": 263
    }, {
        "date": "2012-01-02",
        "buy": 371,
        "sell": 345,
        "total_buy": 482,
        "total_sell": 356
    }, {
        "date": "2012-01-03",
        "buy": 433,
        "sell": 102,
        "total_buy": 562,
        "total_sell": 974
    }, {
        "date": "2012-01-04",
        "buy": 345,
        "sell": 520,
        "total_buy": 379,
        "total_sell": 20
    }, {
        "date": "2012-01-05",
        "buy": 480,
        "sell": 100,
        "total_buy": 501,
        "total_sell": 152
    }, {
        "date": "2012-01-06",
        "buy": 386,
        "sell": 268,
        "total_buy": 443,
        "total_sell": 369
    }, {
        "date": "2012-01-07",
        "buy": 348,
        "sell": 674,
        "total_buy": 405,
        "total_sell": 120
    }, {
        "date": "2012-01-08",
        "buy": 238,
        "sell": 65,
        "total_buy": 309,
        "total_sell": 300
    }, {
        "date": "2012-01-09",
        "buy": 218,
        "sell": 230,
        "total_buy": 287,
        "total_sell": 523
    }, {
        "date": "2012-01-10",
        "buy": 349,
        "sell": 30,
        "total_buy": 485,
        "total_sell": 106
    }, {
        "date": "2012-01-11",
        "buy": 603,
        "sell": 279,
        "total_buy": 890,
        "total_sell": 523
    }, {
        "date": "2012-01-12",
        "buy": 534,
        "sell": 230,
        "total_buy": 810,
        "total_sell": 179
    }, {
        "date": "2012-01-13",
        "buy": 425,
        "sell": 56,
        "total_buy": 670,
        "total_sell": 863
    }];

    // Create axes
    var dateAxis = chart.xAxes.push(new am4charts.DateAxis());
    dateAxis.renderer.grid.template.location = 0;
    dateAxis.renderer.minGridDistance = 50;
    dateAxis.renderer.grid.template.disabled = true;
    dateAxis.renderer.fullWidthTooltip = true;

    var totalAxis = chart.yAxes.push(new am4charts.ValueAxis());
    //totalAxis.title.text = "Total amount";
    totalAxis.renderer.grid.template.disabled = true;
    totalAxis.renderer.opposite = true;
    totalAxis.hidden = true;
    totalAxis.tooltip.disabled = true;


    var totalBuySeries = chart.series.push(new am4charts.LineSeries());
    totalBuySeries.dataFields.valueY = "total_buy";
    totalBuySeries.dataFields.dateX = "date";
    totalBuySeries.yAxis = totalAxis;
    totalBuySeries.name = "Duration";
    totalBuySeries.strokeWidth = 2;
    totalBuySeries.propertyFields.strokeDasharray = "dashLength";
    totalBuySeries.tooltipText = "{valueY} EUR";
    totalBuySeries.showOnInit = true;
    totalBuySeries.fill = am4core.color("green");
    totalBuySeries.stroke = am4core.color("green");

    var totalSellSeries = chart.series.push(new am4charts.LineSeries());
    totalSellSeries.dataFields.valueY = "total_sell";
    totalSellSeries.dataFields.dateX = "date";
    totalSellSeries.yAxis = totalAxis;
    totalSellSeries.name = "Duration";
    totalSellSeries.strokeWidth = 2;
    totalSellSeries.propertyFields.strokeDasharray = "dashLength";
    totalSellSeries.tooltipText = "{valueY} EUR";
    totalSellSeries.showOnInit = true;
    totalSellSeries.fill = am4core.color("red");
    totalSellSeries.stroke = am4core.color("red");

    var durationBullet = totalBuySeries.bullets.push(new am4charts.Bullet());
    var durationRectangle = durationBullet.createChild(am4core.Rectangle);
    durationBullet.horizontalCenter = "middle";
    durationBullet.verticalCenter = "middle";
    durationBullet.width = 7;
    durationBullet.height = 7;
    durationRectangle.width = 7;
    durationRectangle.height = 7;

    var durationState = durationBullet.states.create("hover");
    durationState.properties.scale = 1.2;

    var totalSellBullet = totalSellSeries.bullets.push(new am4charts.Bullet());
    var durationRectangle = totalSellBullet.createChild(am4core.Rectangle);
    totalSellBullet.horizontalCenter = "middle";
    totalSellBullet.verticalCenter = "middle";
    totalSellBullet.width = 7;
    totalSellBullet.height = 7;
    durationRectangle.width = 7;
    durationRectangle.height = 7;

    var totalSellState = totalSellBullet.states.create("hover");
    durationState.properties.scale = 1.2;

    // Add cursor
    chart.cursor = new am4charts.XYCursor();
    chart.cursor.fullWidthLineX = false;
    chart.cursor.xAxis = dateAxis;
    chart.cursor.lineX.strokeOpacity = 0;
    chart.cursor.lineX.fill = am4core.color("#000");
    chart.cursor.lineX.fillOpacity = 0.1;
}



