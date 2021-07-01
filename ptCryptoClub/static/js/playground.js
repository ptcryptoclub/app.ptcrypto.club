

function ohlc_chart(chartDiv, market, base, quote, datapoints, candle, candle_rate) {

    let apiSecret = document.getElementById("APISecret").value;

    // Themes begin
    am4core.useTheme(am4themes_dark);
    // am4core.useTheme(am4themes_animated);
    // Themes end

    var chart = am4core.create(chartDiv, am4charts.XYChart);
    chart.padding(15, 15, 15, 15);

    chart.dateFormatter.inputDateFormat = "yyyy-MM-dd HH:mm:ss";
    chart.leftAxesContainer.layout = "vertical";
    chart.zoomOutButton.disabled = true;

    chart.dataSource.url = '/api/charts/ohlc/' + market + '/' + base + '/' + quote + '/' + datapoints + '/' + candle + '/'  + apiSecret + '/';
    chart.dataSource.load();
    chart.dataSource.keepCount = true;
    chart.dataSource.parser = new am4core.JSONParser();
    chart.dataSource.updateCurrentData = true;
    chart.dataSource.reloadFrequency = candle_rate * 1000;

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

    dateAxis.start = 0.60;
    dateAxis.end = 1;
    dateAxis.keepSelection = true;


    var valueAxis = chart.yAxes.push(new am4charts.ValueAxis());
    valueAxis.tooltip.disabled = true;
    valueAxis.zIndex = 1;
    valueAxis.renderer.baseGrid.disabled = true;
    valueAxis.title.text = base.toUpperCase() + quote.toUpperCase();
    valueAxis.title.fontSize = "0.8em"
    valueAxis.title.fill = am4core.color("#00bbff");
    // height of axis
    valueAxis.height = am4core.percent(90);

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

    var series_mae = chart.series.push(new am4charts.LineSeries());
    series_mae.dataFields.valueY = "moving_exp";
    series_mae.dataFields.dateX = "closetime";
    series_mae.strokeWidth = 1;
    series_mae.stroke = am4core.color("#ffc400");

    /////////////


    var valueAxis2 = chart.yAxes.push(new am4charts.ValueAxis());
    valueAxis2.tooltip.disabled = true;
    // height of axis
    valueAxis2.height = am4core.percent(10);
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
    series2.tooltipText = "Volume: {valueY.value} " + base.toUpperCase();
    series2.fillOpacity = 0.2;
    // volume should be summed
    ///series2.groupFields.valueY = "sum";


    chart.cursor = new am4charts.XYCursor();
    chart.cursor.behavior = "panX";
    chart.cursor.maxPanOut = 0.005
    // Create scrollbars
    chart.scrollbarX = new am4core.Scrollbar();

}

function expandChart(divID) {
    let htmlDIV = document.getElementById(divID);
    htmlDIV.className = "col-lg-12 mt-5";
}


function collapseChart(divID) {
    let htmlDIV = document.getElementById(divID);
    htmlDIV.className = "col-lg-6 mt-5";
}


function closeChart(divID) {
    let htmlDIV = document.getElementById(divID);
    htmlDIV.outerHTML = "";
}


function closeCard(divID) {
    let htmlDIV = document.getElementById("card-" + divID);
    htmlDIV.outerHTML = "";
    if (divID == "1") {
        clearInterval(runUpdates_1);
    } else if (divID == "2") {
        clearInterval(runUpdates_2);
    }
    
}


function buyReport() {
    let market = document.getElementById("market").value;
    let base = document.getElementById("base").value;
    let quote = document.getElementById("quote").value;
    let fee = document.getElementById("chargedFee").value / 100;
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
    let fee = document.getElementById("chargedFee_sell").value / 100;
    let amount_available = document.getElementById("sellAmountAvailable");
    let amount_available_value = document.getElementById("hidden-"+ base +"-value").value;
    let apiSecret = document.getElementById("APISecret").value;

    let max_ = document.getElementById("amount_spent_sell")

    fetch('/api/account/portfolio/price/' + market + '/' + base + '/' + quote + '/' + apiSecret + '/').then(
        function(response2){
            response2.json().then(
                function (data2){
                    price = data2['price']
                    amount_available.innerHTML = amount_available_value + '<small> ' + base.toUpperCase() + '</small>'
                    max_.max = amount_available_value
                    amountSell = document.getElementById("amount_spent_sell").value
                    price_without_feee = (amountSell * price).toFixed(2)
                    amountFee = (price_without_feee * fee).toFixed(2)
                    price_with_fee = (price_without_feee - amountFee).toFixed(2)

                    displayPrice = document.getElementById("price_sell");
                    displayAmount = document.getElementById("amount_sell");
                    displayPriceWithoutFee = document.getElementById("price_without_fee")
                    displayFee = document.getElementById("fee_sell");
                    displayResult = document.getElementById("result_sell");

                    displayPrice.innerHTML = data2['price'] + '<small> ' + quote.toUpperCase() + '</small>'
                    displayAmount.innerHTML = amountSell+ '<small> ' + base.toUpperCase() + '</small>'
                    displayPriceWithoutFee.innerHTML = price_without_feee + '<small> ' + quote.toUpperCase() + '</small>'
                    displayFee.innerHTML = amountFee + '<small> ' + quote.toUpperCase() + '</small>'
                    displayResult.innerHTML = price_with_fee + '<small> ' + quote.toUpperCase() + '</small>'

                }
            )
        }
    )

}


function clearReport() {
    displayPrice = document.getElementById("price");
    displayAmount = document.getElementById("amount");
    displayFee = document.getElementById("fee");
    displayResult = document.getElementById("result");

    displayPrice.innerHTML = "";
    displayAmount.innerHTML = "";
    displayFee.innerHTML = "";
    displayResult.innerHTML = "";
}


function clearReportSell() {
    displayPrice = document.getElementById("price_sell");
    displayAmount = document.getElementById("amount_sell");
    displayPriceWithoutFee = document.getElementById("price_without_fee")
    displayFee = document.getElementById("fee_sell");
    displayResult = document.getElementById("result_sell");

    displayPrice.innerHTML = "";
    displayAmount.innerHTML = "";
    displayPriceWithoutFee.innerHTML = "";
    displayFee.innerHTML = "";
    displayResult.innerHTML = "";
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



function update_values_1 () {
    let borderLine = document.getElementById("generalCard-1");
    let market = document.getElementById("marketCard-1");
    let base = document.getElementById("baseCard-1");
    let quote = document.getElementById("quoteCard-1");
    let delta = document.getElementById("deltaCard-1");
    let change = document.getElementById("changeCard-1");
    let price = document.getElementById("lastCard-1");
    let high = document.getElementById("highCard-1");
    let low = document.getElementById("lowCard-1");
    let volume = document.getElementById("volumeCard-1");
    let volumeQuote = document.getElementById("volumequoteCard-1");
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


function update_values_2 () {
    let borderLine = document.getElementById("generalCard-2");
    let market = document.getElementById("marketCard-2");
    let base = document.getElementById("baseCard-2");
    let quote = document.getElementById("quoteCard-2");
    let delta = document.getElementById("deltaCard-2");
    let change = document.getElementById("changeCard-2");
    let price = document.getElementById("lastCard-2");
    let high = document.getElementById("highCard-2");
    let low = document.getElementById("lowCard-2");
    let volume = document.getElementById("volumeCard-2");
    let volumeQuote = document.getElementById("volumequoteCard-2");
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



function updateCompetitionPortfolio (user_id, compt_id) {
    let apiSecret = document.getElementById("APISecret").value;
    let cv_value = document.getElementById("cv_value");
    let cv_icon = document.getElementById("cv_icon");
    let cv_pct_change = document.getElementById("cv_pct_change");
    
    fetch('/api/competition/calculate-portfolio/' + user_id + '/' + compt_id + '/' + apiSecret + '/').then(
        function(response){
            response.json().then(
                function (data) {

                    cv_value.innerHTML = numberFormat(data["current_value"])

                    if (data["pct_change"] > 0) {
                        cv_icon.innerHTML = '<span class="material-icons text-success" style="font-size:48px">north</span>'
                        cv_pct_change.innerHTML = '<h5>' + data["pct_change"] + '%</h5>'
                        cv_pct_change.className = 'col-auto mr-2 text-success'
                        
                    } else if (data["pct_change"] < 0) {
                        cv_icon.innerHTML = '<span class="material-icons text-danger" style="font-size:48px">south</span>'
                        cv_pct_change.innerHTML = '<h5>' + data["pct_change"] + '%</h5>'
                        cv_pct_change.className = 'col-auto mr-2 text-danger'
                    } else {
                        cv_icon.innerHTML = '<span class="material-icons text-warning" style="font-size:48px">unfold_less</span>'
                        cv_pct_change.innerHTML = '<h5>' + data["pct_change"] + '%</h5>'
                        cv_pct_change.className = 'col-auto mr-2 text-warning'
                    }
                }
            )
        }
    );
}



function historical_line(divName, base, quote, starting_date_chart, ending_date_chart, trans, starting_date, ending_date) {


    


    var apiSecret = document.getElementById("APISecret").value;


    var nowTime = new Date();

    var end_y = nowTime.getUTCFullYear()
    var end_m = parseInt(nowTime.getUTCMonth()) + 1
    var end_d = nowTime.getUTCDate()
    var end_h = nowTime.getUTCHours()
    var end_mm = nowTime.getUTCMinutes()
    var end_s = nowTime.getUTCSeconds()

    var end = ending_date_chart
    // NOT IN USE //
    prefix = 30
    nowTime.setDate(nowTime.getDate() - prefix);
    var start_y = nowTime.getUTCFullYear()
    var start_m = parseInt(nowTime.getUTCMonth()) + 1
    var start_d = nowTime.getUTCDate()
    var start_h = nowTime.getUTCHours()
    var start_mm = nowTime.getUTCMinutes()
    var start_s = nowTime.getUTCSeconds()
    ////////////////

    var start = starting_date_chart

    urlToSend = "/api/historical-charts/line/" + base + "/" + quote + "/kraken/900/" + apiSecret + "/?start=" + start + "&end=" + end;

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

    // Title
    let title = chart.titles.create();
    title.text = base.toUpperCase() + quote.toUpperCase();
    title.fontSize = 16;
    title.marginBottom = 10;



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

    valueAxis.extraMin = 0.02;
    valueAxis.extraMax = 0.02;

    var series = chart.series.push(new am4charts.LineSeries());
    series.dataFields.dateX = "date";
    series.dataFields.valueY = "closeprice";
    // series.tooltipText = "{valueY.value}";
    series.defaultState.transitionDuration = 0;
    series.fillOpacity = 0.2;

    chart.cursor = new am4charts.XYCursor();
    chart.cursor.snapToSeries = series;
    chart.cursor.behavior = "zoomX"

    // vertical line to show competiton start date
    function createEvent(date, text, color) {
        var flag = new am4plugins_bullets.FlagBullet();
        
        flag.label.text = text;
        flag.label.horizontalCenter = "middle";
        flag.label.fontSize = 14;
        
        flag.pole.stroke = color;
        flag.pole.strokeWidth = 2;
        
        flag.background.waveLength = 15;
        flag.background.fill = color;
        flag.background.stroke = color;
        flag.background.strokeWidth = 2;
        flag.background.fillOpacity = 0.6;
        
        var event = dateAxis.axisRanges.create();
        event.date = date;
        event.bullet = flag;
        event.grid.strokeWidth = 0;
        
      }
    createEvent(new Date(starting_date), "Start", am4core.color("#00c43b"));
    createEvent(new Date(ending_date), "End", am4core.color("#c40000"));





    function createDot(data, color, type_, price_, amountSpent_,amountAsset_, date_) {
        var trend = chart.series.push(new am4charts.LineSeries());
        trend.dataFields.valueY = "closeprice";
        trend.dataFields.dateX = "date";
        
        trend.stroke = trend.fill = am4core.color(color);
        trend.data = data;
        
        trend.strokeWidth = 0

        var bullet = trend.bullets.push(new am4charts.CircleBullet());
        
        bullet.strokeWidth = 2;
        bullet.stroke = am4core.color(color)
        bullet.circle.fill = trend.stroke;
        
        // series.tooltip.background.propertyFields.stroke = am4core.color(color);
      
        var hoverState = bullet.states.create("hover");
        hoverState.properties.scale = 1.7;

        bullet.circle.hoverable = true;
        bullet.circle.events.on("over", function(ev) {
            if (type_ == "Buy") {
                series.tooltipText = "Type: " + type_ + "\n" + "Amount spent: " + numberFormat(amountSpent_) + " " + quote.toUpperCase() + "\n" + "Price: " + numberFormat(price_) + " " + quote.toUpperCase() + "\n" + "Asset bought: " + numberFormat(amountAsset_) + " " + base.toUpperCase() + "\n" + "Date: " + date_;
                series.tooltip.getFillFromObject = false;
                series.tooltip.background.fill = am4core.color(color);
            } else {
                series.tooltipText = "Type: " +  type_ + "\n" + "Amount sold: " + numberFormat(amountAsset_) + " " + base.toUpperCase() + "\n" + "Price: " + numberFormat(price_) + " " + quote.toUpperCase() + "\n" + "Amount net: " + numberFormat(amountSpent_) + " " + quote.toUpperCase() + "\n" + "Date: " + date_;
                series.tooltip.getFillFromObject = false;
                series.tooltip.background.fill = am4core.color(color);
            }
            
        })
        bullet.circle.events.on("out", function(ev) {
            series.tooltipText = "";
          })


    };


    chart.dataSource.events.on("done", function (ev) {

        
        for (let i = 0; i < trans.length; i++) {
            if (trans[i]['base'] == base) {
                if (trans[i]['type'] == 'buy') {
                    createDot([{ "date": trans[i]['date_created'], "closeprice": trans[i]['asset_price'] }], "#00c43b", "Buy", trans[i]['asset_price'], trans[i]['amount_gross'], trans[i]['asset_amount'], trans[i]['date_created'])
                } else {
                    createDot([{ "date": trans[i]['date_created'], "closeprice": trans[i]['asset_price'] }], "#c40000", "Sell", trans[i]['asset_price'], trans[i]['amount_net'], trans[i]['asset_amount'], trans[i]['date_created'])
                }
                
            }
            
          } 

    });

    
}