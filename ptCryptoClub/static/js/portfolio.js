
function updatePortfolio(userID) {
    let apiSecret = document.getElementById("APISecret").value;
    let allDiv = document.getElementById("updateAll")
    let divHTML = ''
    fetch('/api/account/portfolio/update-all/' + userID + '/' + apiSecret + '/').then(
        function(response){
            response.json().then(
                function (data){
                    totalValue = data['value'];
                    quote = data['quote'];
                    percentage = data['percentage'];
                    divHTML += '<div class="col-auto"><H1 class="display-4 text-light"><small>'+ numberFormat(totalValue) +'</small></H1></div><div class="col-auto"><small class="text-light">'+ quote.toUpperCase() +'</small></div>'
                    if (percentage > 0) {
                        divHTML +='<div class="col-auto"><span class="material-icons text-success" style="font-size:48px">north</span></div><div class="col-auto mr-2 text-success"><h5>'+ percentage +'%</h5></div>'
                    } else if (percentage < 0) {
                        divHTML +='<div class="col-auto"><span class="material-icons text-danger" style="font-size:48px">south</span></div><div class="col-auto mr-2 text-danger"><h5>'+ percentage +'%</h5></div>'
                    }
                    else {
                        divHTML +='<div class="col-auto"><span class="material-icons text-warning" style="font-size:48px">unfold_less</span></div><div class="col-auto mr-2 text-warning"><h5>'+ percentage +'%</h5></div>'
                    }
                    allDiv.innerHTML = divHTML
                }
            )
        }
    )
}


function buyReport() {
    let market = document.getElementById("market").value;
    let base = document.getElementById("base").value;
    let quote = document.getElementById("quote").value;
    let fee = document.getElementById("chargedFee").value;
    let apiSecret = document.getElementById("APISecret").value;
    fetch('/api/account/portfolio/price/' + market + '/' + base + '/' + quote + '/' + apiSecret + '/').then(
        function(response){
            response.json().then(
                function (data){
                    price = data['price']
                    amountSpent = document.getElementById("amount_spent").value
                    amountFee = (amountSpent * fee).toFixed(2)
                    amountAsset = (amountSpent - amountFee)/price

                    displayPrice = document.getElementById("price");
                    displayAmount = document.getElementById("amount");
                    displayFee = document.getElementById("fee");
                    displayResult = document.getElementById("result");

                    displayPrice.innerHTML = numberFormat(price) + ' <small>' + quote.toUpperCase() + '</small>';
                    displayAmount.innerHTML = numberFormat(amountSpent) + ' <small>' + quote.toUpperCase() + '</small>';
                    displayFee.innerHTML = numberFormat(amountFee) + ' <small>' + quote.toUpperCase() + '</small>';
                    displayResult.innerHTML = numberFormat(amountAsset.toFixed(8)) + ' <small>' + base.toUpperCase() + '</small>';
                }
            )
        }
    )
}


function sellReport() {
    let market = document.getElementById("market_sell").value;
    let base = document.getElementById("base_sell").value;
    let quote = document.getElementById("quote_sell").value;
    let fee = document.getElementById("chargedFee").value;
    let amount_available = document.getElementById("sellAmountAvailable");
    let amount_available_value = document.getElementById("hidden-"+ base +"-value").value;
    let apiSecret = document.getElementById("APISecret").value;
    fetch('/api/account/portfolio/price/' + market + '/' + base + '/' + quote + '/' + apiSecret + '/').then(
        function(response2){
            response2.json().then(
                function (data2){
                    price = data2['price']
                    amount_available.innerHTML = amount_available_value + '<small>' + base.toUpperCase() + '</small>'
                    amountSell = document.getElementById("amount_spent_sell").value
                    price_without_feee = (amountSell * price).toFixed(8)
                    amountFee = (price_without_feee * fee).toFixed(8)
                    price_with_fee = (price_without_feee - amountFee).toFixed(8)

                    displayPrice = document.getElementById("price_sell");
                    displayAmount = document.getElementById("amount_sell");
                    displayPriceWithoutFee = document.getElementById("price_without_fee")
                    displayFee = document.getElementById("fee_sell");
                    displayResult = document.getElementById("result_sell");

                    displayPrice.innerHTML = data2['price'] + '<small> ' + quote.toUpperCase() + '</small>'
                    displayAmount.innerHTML = amountSell
                    displayPriceWithoutFee.innerHTML = price_without_feee
                    displayFee.innerHTML = amountFee
                    displayResult.innerHTML = price_with_fee

                }
            )
        }
    )

}


function updateBase() {
    let market = document.getElementById("market").value;
    let base_select = document.getElementById("base");
    let apiSecret = document.getElementById("APISecret").value;
    fetch('/api/account/portfolio/dropdowns/base/' + market + '/' + apiSecret + '/').then(
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


function updateBaseSell() {
    let market = document.getElementById("market_sell").value;
    let base_select_sell = document.getElementById("base_sell");
    let apiSecret = document.getElementById("APISecret").value;
    fetch('/api/account/portfolio/dropdowns/base/' + market + '/' + apiSecret + '/').then(
        function(response){
            response.json().then(
                function (data){
                    let linesHTML = '';
                    for (let line of data) {
                        linesHTML += '<option value="' + line['base'] + '">' + line['base'].toUpperCase() + '</option>'
                    }
                    base_select_sell.innerHTML = linesHTML
                }
            )
        }
    )
}


function updateQuote() {
    let market = document.getElementById("market").value;
    let base = document.getElementById("base").value;
    let quote_select = document.getElementById("quote");
    let apiSecret = document.getElementById("APISecret").value;
    if (base === '') {

    } else {
        fetch('/api/account/portfolio/dropdowns/quote/' + market + '/' + base + '/' + apiSecret + '/').then(
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


function updateQuoteSell() {
    let market = document.getElementById("market_sell").value;
    let base = document.getElementById("base_sell").value;
    let quote_select = document.getElementById("quote_sell");
    let apiSecret = document.getElementById("APISecret").value;
    if (base === '') {

    } else {
        fetch('/api/account/portfolio/dropdowns/quote/' + market + '/' + base + '/' + apiSecret + '/').then(
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


function pieWalletAssets(divName, portfolioData) {
    // Create chart instance
    var chart = am4core.create(divName, am4charts.PieChart);

    // Add data
    chart.data = [ {
      "type": "Wallet",
      "value": portfolioData['wallet'],
      "color": am4core.color("#235789")
    }, {
      "type": "Assets",
      "value": portfolioData['assets'],
      "color": am4core.color("#F1D302")
    }];

    // Set inner radius
    chart.innerRadius = am4core.percent(50);

    // Add legend
    chart.legend = new am4charts.Legend();
    chart.legend.useDefaultMarker = true;
    chart.legend.position = "right";
    chart.legend.labels.template.fill = am4core.color("white");

    let marker = chart.legend.markers.template.children.getIndex(0);
    marker.cornerRadius(12, 12, 12, 12);
    marker.strokeWidth = 2;
    marker.strokeOpacity = 1;
    marker.stroke = am4core.color("#ccc");
    

    // Add and configure Series
    var pieSeries = chart.series.push(new am4charts.PieSeries());
    pieSeries.dataFields.value = "value";
    pieSeries.dataFields.category = "type";
    pieSeries.slices.template.propertyFields.fill = "color";
    pieSeries.slices.template.stroke = am4core.color("#fff");
    pieSeries.slices.template.strokeWidth = 2;
    pieSeries.slices.template.strokeOpacity = 1;

    pieSeries.labels.template.disabled = true;
    pieSeries.ticks.template.disabled = true;


    // This creates initial animation
    pieSeries.hiddenState.properties.opacity = 1;
    pieSeries.hiddenState.properties.endAngle = -90;
    pieSeries.hiddenState.properties.startAngle = -90;
}

// NOT IN USE //
function pieAssets(divName, assetsData) {
    // Create chart instance
    var chart = am4core.create(divName, am4charts.PieChart);

    // Add data
    chart.data = assetsData;

    // Set inner radius
    chart.innerRadius = am4core.percent(50);

    // Add and configure Series
    var pieSeries = chart.series.push(new am4charts.PieSeries());
    pieSeries.dataFields.value = "amount";
    pieSeries.dataFields.category = "base";
    pieSeries.slices.template.stroke = am4core.color("#fff");
    pieSeries.slices.template.strokeWidth = 2;
    pieSeries.slices.template.strokeOpacity = 1;

    // This creates initial animation
    pieSeries.hiddenState.properties.opacity = 1;
    pieSeries.hiddenState.properties.endAngle = -90;
    pieSeries.hiddenState.properties.startAngle = -90;
}


function lineBuySell(divName, user_ID, numberDays) {
    let apiSecret = document.getElementById("APISecret").value;

    // Themes begin
    am4core.useTheme(am4themes_dark);
    am4core.useTheme(am4themes_animated);
    // Themes end

    // Create chart instance
    var chart = am4core.create(divName, am4charts.XYChart);
    chart.dateFormatter.inputDateFormat = "yyyy-MM-dd HH:mm:ss";

    chart.colors.step = 2;
    chart.maskBullets = false;

    // Add data
    chart.dataSource.url = '/api/account/portfolio/line-chart/'+ user_ID +'/'+ numberDays +'/'+ apiSecret +'/';
    chart.dataSource.load();

    // Create axes
    var dateAxis = chart.xAxes.push(new am4charts.DateAxis());
    dateAxis.renderer.grid.template.location = 0;
    dateAxis.renderer.minGridDistance = 50;
    dateAxis.renderer.grid.template.disabled = true;
    dateAxis.renderer.fullWidthTooltip = true;
    dateAxis.renderer.fontSize = "0.8em";

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
    totalBuySeries.name = "Buy";
    totalBuySeries.strokeOpacity = 0;
    totalBuySeries.strokeWidth = 2;
    totalBuySeries.propertyFields.strokeDasharray = "dashLength";
    totalBuySeries.tooltipText = "Buy: {valueY} EUR";
    totalBuySeries.showOnInit = true;
    totalBuySeries.fill = am4core.color("green");
    totalBuySeries.stroke = am4core.color("green");

    var totalSellSeries = chart.series.push(new am4charts.LineSeries());
    totalSellSeries.dataFields.valueY = "total_sell";
    totalSellSeries.dataFields.dateX = "date";
    totalSellSeries.yAxis = totalAxis;
    totalSellSeries.name = "Sell";
    totalSellSeries.strokeOpacity = 0;
    totalSellSeries.strokeWidth = 2;
    totalSellSeries.propertyFields.strokeDasharray = "dashLength";
    totalSellSeries.tooltipText = "Sell: {valueY} EUR";
    totalSellSeries.showOnInit = true;
    totalSellSeries.fill = am4core.color("red");
    totalSellSeries.stroke = am4core.color("red");

    var durationBullet = totalBuySeries.bullets.push(new am4charts.Bullet());
    var durationRectangle = durationBullet.createChild(am4core.Rectangle);
    durationBullet.horizontalCenter = "middle";
    durationBullet.verticalCenter = "middle";
    durationBullet.width = 12;
    durationBullet.height = 12;
    durationRectangle.width = 12;
    durationRectangle.height = 12;

    var durationState = durationBullet.states.create("hover");
    durationState.properties.scale = 1.2;

    var totalSellBullet = totalSellSeries.bullets.push(new am4charts.Bullet());
    var durationRectangle = totalSellBullet.createChild(am4core.Rectangle);
    totalSellBullet.horizontalCenter = "middle";
    totalSellBullet.verticalCenter = "middle";
    totalSellBullet.width = 12;
    totalSellBullet.height = 12;
    durationRectangle.width = 12;
    durationRectangle.height = 12;

    var totalSellState = totalSellBullet.states.create("hover");
    totalSellState.properties.scale = 1.2;


    // Add cursor
    chart.cursor = new am4charts.XYCursor();
    chart.cursor.fullWidthLineX = false;
    chart.cursor.xAxis = dateAxis;
    chart.cursor.lineX.strokeOpacity = 0;
    chart.cursor.lineX.fill = am4core.color("#000");
    chart.cursor.lineX.fillOpacity = 0.1;
}



function portfolioChart(divName, user_ID, days) {
    let apiSecret = document.getElementById("APISecret").value;

    // Themes begin
    am4core.useTheme(am4themes_dark);
    am4core.useTheme(am4themes_animated);
    // Themes end

    // Create chart instance
    var chart = am4core.create(divName, am4charts.XYChart);
    chart.zoomOutButton.disabled = false;

    // Add data 
    chart.dataSource.url = '/api/account/portfolio/chart/'+ days +'/'+ user_ID +'/'+ apiSecret +'/';

    // Set input format for the dates
    chart.dateFormatter.inputDateFormat = "yyyy-MM-dd HH:mm:ss";


    // Create axes
    var dateAxis = chart.xAxes.push(new am4charts.DateAxis());
    dateAxis.renderer.fontSize = "0.8em";
    dateAxis.renderer.grid.template.disabled = true;
    dateAxis.tooltip.disabled = true;
    dateAxis.keepSelection = true;

    var valueAxis = chart.yAxes.push(new am4charts.ValueAxis());
    valueAxis.renderer.fontSize = "0.8em";
    valueAxis.renderer.grid.template.disabled = true;
    valueAxis.tooltip.disabled = true;
    valueAxis.title.text = 'EUR';
    valueAxis.title.fontSize = "0.8em";
    valueAxis.renderer.inside = true;

       

    // Create series
    var series = chart.series.push(new am4charts.LineSeries());
    series.dataFields.valueY = "value";
    series.dataFields.dateX = "date";
    series.tooltipText = "[font-size: 0.85em;]Value: {value} EUR\nChange to previous\nAbsolute: {valueY.previousChange} EUR\nPercentage: {valueY.previousChangePercent} %"
    series.strokeWidth = 2;
    //series.minBulletDistance = 15;


    // Make bullets grow on hover
    var bullet = series.bullets.push(new am4charts.CircleBullet());
    bullet.circle.strokeWidth = 2;
    bullet.circle.radius = 4;
    bullet.circle.fill = am4core.color("#fff");

    var bullethover = bullet.states.create("hover");
    bullethover.properties.scale = 1.3;

    // Make a panning cursor
    chart.cursor = new am4charts.XYCursor();
    // chart.cursor.behavior = "panX";


}


function portfolioChartFull (divName, user_ID) {

    let apiSecret = document.getElementById("APISecret").value;
    let days = document.getElementById("deltaDays").value;

    // Themes begin
    am4core.useTheme(am4themes_animated);
    am4core.useTheme(am4themes_dark);
    // Themes end

    // Auto dispose charts
    am4core.options.autoDispose = true;

    var chart = am4core.create(divName, am4charts.XYChart);

    chart.colors.step = 5;

    // Add data 
    chart.dataSource.url = '/api/account/portfolio/chart/'+ days +'/'+ user_ID +'/'+ apiSecret +'/';

    chart.dateFormatter.inputDateFormat = "yyyy-MM-dd HH:mm:ss";
    var dateAxis = chart.xAxes.push(new am4charts.DateAxis());
    dateAxis.renderer.minGridDistance = 60;
    dateAxis.renderer.grid.template.strokeOpacity = 0;
    dateAxis.startLocation = 0.5;
    dateAxis.endLocation = 0.5;
    dateAxis.title.fontSize = "0.8em";
    dateAxis.renderer.fontSize = "0.8em";
    dateAxis.tooltip.disabled = true;


    var valueAxis = chart.yAxes.push(new am4charts.ValueAxis());
    valueAxis.tooltip.disabled = true;
    valueAxis.title.text = 'EUR';
    valueAxis.title.fontSize = "0.8em";
    valueAxis.renderer.fontSize = "0.8em";

    
    var walletSeries = chart.series.push(new am4charts.LineSeries());
    walletSeries.name = "Wallet";
    walletSeries.dataFields.dateX = "date";
    walletSeries.dataFields.valueY = "wallet";
    // walletSeries.tooltipHTML = "<img src='/static/crypto_icons/color/eur.png' style='vertical-align:text-top; margin-right: 10px; width:21px; height:21px;'><span style='font-size:14px; color:#000000;'><b>{valueY.value}</b></span>";
    walletSeries.tooltipText = "[font-size: 0.85em; #000]Wallet: {valueY.value} EUR[/]";
    walletSeries.tooltip.background.fill = am4core.color("#FFF");
    walletSeries.tooltip.getFillFromObject = false;
    walletSeries.tooltip.getStrokeFromObject = true;
    walletSeries.tooltip.background.strokeWidth = 1;
    walletSeries.sequencedInterpolation = true;
    walletSeries.fillOpacity = 0.05;
    walletSeries.strokeWidth = 2;


    var assetsSeries = chart.series.push(new am4charts.LineSeries());
    assetsSeries.dataFields.dateX = "date";
    assetsSeries.name = "Assets";
    assetsSeries.dataFields.valueY = "assets";
    // assetsSeries.tooltipHTML = "<img src='/static/crypto_icons/color/btc.png' style='vertical-align:text-top; margin-right: 10px; width:21px; height:21px;'><span style='font-size:14px; color:#000000;'><b>{valueY.value}</b></span>";
    assetsSeries.tooltipText = "[font-size: 0.85em; #000]Assest: {valueY.value} EUR[/]";
    assetsSeries.tooltip.background.fill = am4core.color("#FFF");
    assetsSeries.tooltip.getStrokeFromObject = true;
    assetsSeries.tooltip.background.strokeWidth = 1;
    assetsSeries.tooltip.getFillFromObject = false;
    assetsSeries.fillOpacity = 0.05;
    assetsSeries.strokeWidth = 2;
    // assetsSeries.stacked = true;


    var totalSeries = chart.series.push(new am4charts.LineSeries());
    totalSeries.dataFields.dateX = "date";
    totalSeries.name = "Total";
    totalSeries.dataFields.valueY = "value";
    totalSeries.tooltipText = "[font-size: 0.85em; #000]Total: {valueY.value} EUR\n\nChange to start\nAbsolute: {valueY.change} EUR\nPercentage: {valueY.changePercent}%[/]";
    totalSeries.tooltip.background.fill = am4core.color("#FFF");
    totalSeries.tooltip.getStrokeFromObject = true;
    totalSeries.tooltip.background.strokeWidth = 1;
    totalSeries.tooltip.getFillFromObject = false;
    totalSeries.fillOpacity = 0.05;
    totalSeries.strokeWidth = 2;

    chart.cursor = new am4charts.XYCursor();
    // chart.cursor.snapToSeries = [assetsSeries, walletSeries];

    /* Add legend */
    chart.legend = new am4charts.Legend();
    chart.legend.useDefaultMarker = true;

    let marker = chart.legend.markers.template.children.getIndex(0);
    marker.cornerRadius(12, 12, 12, 12);
    marker.strokeWidth = 2;
    marker.strokeOpacity = 1;

}


function portfolioChartStart (divName, data) {
    // Themes begin
    am4core.useTheme(am4themes_animated);
    am4core.useTheme(am4themes_dark);
    // Themes end

    // Create chart instance
    var chart = am4core.create(divName, am4charts.XYChart);
    chart.hiddenState.properties.opacity = 0; // this creates initial fade-in

    chart.data = data;

    var categoryAxis = chart.yAxes.push(new am4charts.CategoryAxis());
    categoryAxis.dataFields.category = "name";
    categoryAxis.renderer.grid.template.strokeOpacity = 0;
    categoryAxis.cursorTooltipEnabled = false;
    categoryAxis.renderer.fontSize = "0.8em";
    

    var valueAxis = chart.xAxes.push(new am4charts.ValueAxis());
    valueAxis.renderer.inside = true;
    valueAxis.renderer.labels.template.fillOpacity = 0.3;
    valueAxis.renderer.grid.template.strokeOpacity = 0;
    valueAxis.min = 0;
    valueAxis.cursorTooltipEnabled = false;
    valueAxis.renderer.baseGrid.strokeOpacity = 0;
    valueAxis.hidden = true;

    var series = chart.series.push(new am4charts.ColumnSeries);
    series.dataFields.valueX = "value";
    series.dataFields.categoryY = "name";
    series.tooltipText = "[font-size: 0.85em;]{valueX.value} EUR[/]";
    series.tooltip.pointerOrientation = "vertical";

    var columnTemplate = series.columns.template;
    columnTemplate.height = am4core.percent(25);
    columnTemplate.column.cornerRadius(0, 60, 0, 60);
    columnTemplate.strokeOpacity = 0;

    var cursor = new am4charts.XYCursor();
    chart.cursor = cursor;
    cursor.lineX.disabled = true;
    cursor.lineY.disabled = true;
    cursor.behavior = "none";
}


function portfolioChartFull_2 (divName, user_ID) {

    let apiSecret = document.getElementById("APISecret").value;
    let days = document.getElementById("deltaDays").value;


    // Themes begin
    am4core.useTheme(am4themes_dark);
    am4core.useTheme(am4themes_animated);
    // Themes end

    // Auto dispose charts
    am4core.options.autoDispose = true;

    // Create chart instance
    var chart = am4core.create(divName, am4charts.XYChart);
    chart.colors.step = 5;

    // Add data 
    chart.dataSource.url = '/api/account/portfolio/chart/'+ days +'/'+ user_ID +'/'+ apiSecret +'/';

    // Create axes
    var categoryAxis = chart.xAxes.push(new am4charts.CategoryAxis());
    categoryAxis.dataFields.category = "date";
    categoryAxis.title.text = "Date";
    categoryAxis.renderer.grid.template.location = 0;
    categoryAxis.renderer.minGridDistance = 20;
    categoryAxis.title.fontSize = "0.8em";
    categoryAxis.renderer.fontSize = "0.8em";

    categoryAxis.startLocation = 0.5;
    categoryAxis.endLocation = 0.5;

    categoryAxis.hidden = true;
    categoryAxis.cursorTooltipEnabled = true;

    /* Configure axis tooltip */
    var axisTooltip = categoryAxis.tooltip;
    axisTooltip.background.fill = am4core.color("#fff");
    axisTooltip.background.strokeWidth = 0;
    axisTooltip.background.cornerRadius = 3;
    axisTooltip.background.pointerLength = 0;
    axisTooltip.fontSize = "0.8em";
    axisTooltip.dy = 8;


    var  valueAxis = chart.yAxes.push(new am4charts.ValueAxis());
    valueAxis.title.text = "Percent";
    valueAxis.calculateTotals = true;
    valueAxis.min = 0;
    valueAxis.max = 100;
    valueAxis.strictMinMax = true;
    valueAxis.renderer.labels.template.adapter.add("text", function(text) {
    return text + "%";
    });
    valueAxis.cursorTooltipEnabled = false;
    valueAxis.title.fontSize = "0.8em";
    valueAxis.renderer.fontSize = "0.8em";

    // Create series
    var series = chart.series.push(new am4charts.LineSeries());
    series.dataFields.valueY = "wallet";
    series.dataFields.valueYShow = "totalPercent";
    series.dataFields.categoryX = "date";
    series.name = "Wallet";

    series.tooltipText = "[font-size: 0.85em; #000]Wallet: {valueY.value} EUR[/]";
    series.tooltip.background.fill = am4core.color("#FFF");
    series.tooltip.getFillFromObject = false;
    series.tooltip.getStrokeFromObject = true;
    series.tooltip.background.strokeWidth = 1;
    series.sequencedInterpolation = true;
    series.strokeWidth = 2;

    series.fillOpacity = 0.20;
    series.stacked = true;

    // static
    series.legendSettings.labelText = "Wallet";
    // series.legendSettings.valueText = "{valueY.close}";

    // hovering
    // series.legendSettings.itemLabelText = "Cars:";
    // series.legendSettings.itemValueText = "{valueY}";

    var series2 = chart.series.push(new am4charts.LineSeries());
    series2.dataFields.valueY = "assets";
    series2.dataFields.valueYShow = "totalPercent";
    series2.dataFields.categoryX = "date";
    series2.name = "Assets";

    series2.tooltipText = "[font-size: 0.85em; #000]Assets: {valueY.value} EUR[/]";
    series2.tooltip.background.fill = am4core.color("#FFF");
    series2.tooltip.getFillFromObject = false;
    series2.tooltip.getStrokeFromObject = true;
    series2.tooltip.background.strokeWidth = 1;
    series2.sequencedInterpolation = true;
    series2.strokeWidth = 2;

    series2.fillOpacity = 0.20;
    series2.stacked = true;

    // static
    series2.legendSettings.labelText = "Assets";
    // series2.legendSettings.valueText = "{valueY.close}";

    // hovering
    // series2.legendSettings.itemLabelText = "Motorcycles:";
    // series2.legendSettings.itemValueText = "{valueY}";

    // Add cursor
    chart.cursor = new am4charts.XYCursor();

    // add legend
    chart.legend = new am4charts.Legend();
    chart.legend.useDefaultMarker = true;

    let marker = chart.legend.markers.template.children.getIndex(0);
    marker.cornerRadius(12, 12, 12, 12);
    marker.strokeWidth = 2;
    marker.strokeOpacity = 1;
}


