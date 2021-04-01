
function pageClock() {
    var today = new Date();
    var h = today.getUTCHours();
    var m = today.getUTCMinutes();
    var s = today.getUTCSeconds();
    h = checkTime(h)
    m = checkTime(m);
    s = checkTime(s);
    document.getElementById('clock').innerHTML =
        h + ":" + m + ":" + s;
    var t = setTimeout(pageClock, 500);
}

function checkTime(i) {
    if (i < 10) { i = "0" + i };  // add zero in front of numbers < 10
    return i;
}

function numberFormat(to_format) {
    var parts = to_format.toString().split(".");
    parts[0] = parts[0].replace(/\B(?=(\d{3})+(?!\d))/g, ",");
    return parts.join(".");
}

// NOT IN USE //
function smallChart(divID, base, quote, market, delta) {
    // Themes begin
    am4core.useTheme(am4themes_dark);
    am4core.useTheme(am4themes_animated);
    // Themes end

    // Create chart
    var chart = am4core.create(divID, am4charts.XYChart);
    chart.dateFormatter.inputDateFormat = "yyyy-MM-dd HH:mm:ss";


    chart.dataSource.url = '/api/home/cards/small-chart/' + base + '/' + quote + '/' + market + '/' + delta + '/'
    chart.dataSource.load();
    chart.dataSource.parser = new am4core.JSONParser();

    var dateAxis = chart.xAxes.push(new am4charts.DateAxis());
    dateAxis.tooltip.disabled = true;
    dateAxis.renderer.grid.template.disabled = true;
    dateAxis.renderer.labels.template.disabled = true

    var valueAxis = chart.yAxes.push(new am4charts.ValueAxis());
    valueAxis.tooltip.disabled = true;
    valueAxis.renderer.grid.template.disabled = true;
    valueAxis.renderer.labels.template.disabled = true

    var series = chart.series.push(new am4charts.LineSeries());
    series.dataFields.dateX = "date";
    series.dataFields.valueY = "close";
    series.fillOpacity = 0.08;
    // series.fill = 'green'
    // series.stroke = 'green'


    chart.cursor = new am4charts.XYCursor();
    //chart.cursor.lineY.opacity = 0;
    //chart.cursor.lineX.opacity = 0;
    chart.cursor.behavior = "none";
}


function cardUpdate(base, quote, market, delta) {

    let generalID = document.getElementById("general-"+ market +"-"+ base +"-"+ quote);
    let changeID = document.getElementById("change-"+ market +"-"+ base +"-"+ quote);
    let lastID = document.getElementById("last-"+ market +"-"+ base +"-"+ quote);
    let highID = document.getElementById("high-"+ market +"-"+ base +"-"+ quote);
    let lowID = document.getElementById("low-"+ market +"-"+ base +"-"+ quote);
    let volumeID = document.getElementById("volume-"+ market +"-"+ base +"-"+ quote);
    let volumeQuoteID = document.getElementById("volumeQuote-"+ market +"-"+ base +"-"+ quote);
    let apiSecret = document.getElementById("APISecret").value;

    fetch('/api/home/cards/'+ base +'/'+ quote +'/'+ market +'/'+ delta +'/'+ apiSecret +'/').then(
        function(response){
            response.json().then(
                function (data) {
                    changeID.innerHTML = data['change'] + '%';
                    if (data['change'] < 0) {
                        generalID.className = 'p-2 border border-danger rounded-lg'
                        changeID.className = 'text-danger ml-3'
                        lastID.className = 'text-right text-danger'
                    } else if (data['change'] === 0) {
                        generalID.className = 'p-2 border border-warning rounded-lg'
                        changeID.className = 'text-warning ml-3'
                        lastID.className = 'text-right text-warning'
                    } else {
                        generalID.className = 'p-2 border border-success rounded-lg'
                        changeID.className = 'text-success ml-3'
                        lastID.className = 'text-right text-success'
                    }
                    lastID.innerHTML = numberFormat(data['last_price']);
                    highID.innerHTML = '<strong>High: </strong>' + numberFormat(data['high']);
                    lowID.innerHTML = '<strong>Low: </strong>' + numberFormat(data['low']);
                    volumeID.innerHTML = numberFormat(data['volume']) + ' ' + base.toUpperCase();
                    volumeQuoteID.innerHTML = numberFormat(data['volume_quote']) + ' ' + quote.toUpperCase();
                }
            )
        }
    );
};


function tableUpdate(base, quote, market, number_of_trans, elementId) {

    let tableId = document.getElementById(elementId);
    let apiSecret = document.getElementById("APISecret").value;

    fetch('/api/home/latest-transactions/'+ base +'/'+ quote +'/'+ market +'/'+ number_of_trans +'/'+ apiSecret +'/').then(function(response) {
        response.json().then(function(data) {
            let linesHTML = '';
            for (let line of data) {
                linesHTML += '<tr><td class="d-none d-sm-none d-md-table-cell">' + line['ind'] +'</td><td>' + line['base'].toUpperCase() + line['quote'].toUpperCase() +'</td><td class="text-center">' + line['date'] +'</td><td class="text-right">' + numberFormat(line['amount']) +'</td><td class="text-right">' + numberFormat(line['price']) +'</td></tr>'
            }
            tableId.innerHTML = linesHTML
        })
    })
}


function printpage() {
    //Print the page content
    window.print()
}


function cciGauge(divName, initValue, market_1, base_1, quote_1, market_2, base_2, quote_2, delta) {

    let apiSecret = document.getElementById("APISecret").value;

    // Themes begin
    am4core.useTheme(am4themes_dark);
    am4core.useTheme(am4themes_animated);
    // Themes end

    var chartMin = 0;
    var chartMax = 100;

    var data = {
    score: initValue,
    gradingData: [
        {
        color: "#f04922",
        lowScore: 0,
        highScore: 30
        },
        {
        color: "#fdae19",
        lowScore: 30,
        highScore: 50
        },
        {
        color: "#f3eb0c",
        lowScore: 50,
        highScore: 70
        },
        {
        color: "#b0d136",
        lowScore: 70,
        highScore: 90
        },
        {
        color: "#0f9747",
        lowScore: 90,
        highScore: 100
        }
    ]
    };

    // Grading Lookup
    function lookUpGrade(lookupScore, grades) {
    // Only change code below this line
    for (var i = 0; i < grades.length; i++) {
        if (
        grades[i].lowScore < lookupScore &&
        grades[i].highScore >= lookupScore
        ) {
        return grades[i];
        }
    }
    return null;
    }

    // create chart
    var chart = am4core.create(divName, am4charts.GaugeChart);
    chart.hiddenState.properties.opacity = 0;
    chart.fontSize = 11;
    chart.innerRadius = am4core.percent(90);
    chart.resizable = true;

    // Normal axis
    var axis = chart.xAxes.push(new am4charts.ValueAxis());
    axis.min = chartMin;
    axis.max = chartMax;
    axis.strictMinMax = true;
    axis.renderer.radius = am4core.percent(80);
    axis.renderer.inside = true;
    axis.renderer.line.strokeOpacity = 0.1;
    axis.renderer.ticks.template.disabled = false;
    axis.renderer.ticks.template.strokeOpacity = 1;
    axis.renderer.ticks.template.strokeWidth = 0.5;
    axis.renderer.ticks.template.length = 5;
    axis.renderer.grid.template.disabled = true;
    axis.renderer.labels.template.radius = am4core.percent(15);
    axis.renderer.labels.template.fontSize = "0.9em";
    axis.hidden = true;


    // Axis for ranges
    var axis2 = chart.xAxes.push(new am4charts.ValueAxis());
    axis2.min = chartMin;
    axis2.max = chartMax;
    axis2.strictMinMax = true;
    axis2.renderer.labels.template.disabled = true;
    axis2.renderer.ticks.template.disabled = true;
    axis2.renderer.grid.template.disabled = false;
    axis2.renderer.grid.template.opacity = 0.5;
    axis2.renderer.labels.template.bent = true;
    axis2.renderer.labels.template.fill = am4core.color("#000");
    axis2.renderer.labels.template.fontWeight = "bold";
    axis2.renderer.labels.template.fillOpacity = 0.3;

    // Ranges
    for (let grading of data.gradingData) {
    var range = axis2.axisRanges.create();
    range.axisFill.fill = am4core.color(grading.color);
    range.axisFill.fillOpacity = 0.8;
    range.axisFill.zIndex = -1;
    range.value = grading.lowScore > chartMin ? grading.lowScore : chartMin;
    range.endValue = grading.highScore < chartMax ? grading.highScore : chartMax;
    range.grid.strokeOpacity = 0;
    range.stroke = am4core.color(grading.color).lighten(-0.1);
    range.label.inside = true;
    range.label.inside = true;
    range.label.location = 0.5;
    range.label.inside = true;
    range.label.radius = am4core.percent(10);
    range.label.paddingBottom = -5; // ~half font size
    range.label.fontSize = "0.9em";
    }

    var matchingGrade = lookUpGrade(data.score, data.gradingData);

    // Label 1
    var label = chart.radarContainer.createChild(am4core.Label);
    label.isMeasured = false;
    label.fontSize = "3em";
    label.x = am4core.percent(50);
    label.horizontalCenter = "middle";
    label.verticalCenter = "bottom";
    label.text = data.score.toFixed(1);
    label.fill = am4core.color(matchingGrade.color);

    // Hand
    var hand = chart.hands.push(new am4charts.ClockHand());
    hand.axis = axis2;
    hand.innerRadius = am4core.percent(55);
    hand.startWidth = 8;
    hand.pin.disabled = true;
    hand.value = data.score;
    hand.fill = am4core.color("#444");
    hand.stroke = am4core.color("#000");

    hand.events.on("positionchanged", function(){
    label.text = axis2.positionToValue(hand.currentPosition).toFixed(1);
    var value2 = axis.positionToValue(hand.currentPosition);
    var matchingGrade = lookUpGrade(axis.positionToValue(hand.currentPosition), data.gradingData); 
    label.fill = am4core.color(matchingGrade.color);
    })

    setInterval(function() {
        fetch('/api/home/cci/'+ market_1 +'/'+ base_1 +'/'+ quote_1 +'/'+ market_2 +'/'+ base_2 +'/'+ quote_2 +'/'+ delta +'/'+ apiSecret +'/').then(function(response) {
            response.json().then(function(data) {
                var value = data['cci'] * 100;
                hand.showValue(value, 1000, am4core.ease.cubicOut);
            })
        })
    }, 60*1000);
}


function cciChart(divName, market_1, base_1, quote_1, market_2, base_2, quote_2){

    let apiSecret = document.getElementById("APISecret").value;
    // Themes begin
    am4core.useTheme(am4themes_dark);
    am4core.useTheme(am4themes_animated);
    // Themes end

    // Create chart
    var chart = am4core.create(divName, am4charts.XYChart);
    chart.paddingRight = 20;
    chart.dateFormatter.inputDateFormat = "yyyy-MM-dd HH:mm:ss";
    chart.dataSource.url = '/api/home/cci/chart/'+ market_1 +'/'+ base_1 +'/'+ quote_1 +'/'+ market_2 +'/'+ base_2 +'/'+ quote_2 +'/100/'+ apiSecret +'/'
    chart.dataSource.load();
    chart.dataSource.parser = new am4core.JSONParser();


    var dateAxis = chart.xAxes.push(new am4charts.DateAxis());
    dateAxis.renderer.fontSize = "0.7em";
    dateAxis.renderer.grid.template.disabled = true;
    dateAxis.tooltip.disabled = true;


    var valueAxis = chart.yAxes.push(new am4charts.ValueAxis());
    valueAxis.renderer.fontSize = "0.7em";
    valueAxis.tooltip.disabled = true;
    valueAxis.renderer.grid.template.disabled = true;

    var series = chart.series.push(new am4charts.LineSeries());
    series.dataFields.dateX = "date";
    series.dataFields.valueY = "cci";
    series.tooltipText = "{valueY.value}";
    series.strokeWidth = 1.5;
    series.fillOpacity = 0.2;

    chart.cursor = new am4charts.XYCursor();
    chart.cursor.snapToSeries = series;

    let title = chart.titles.create();
    title.text = "CCI (last 24h)";
    title.fontSize = "0.7em";
    title.marginBottom = 2;

    valueAxis.numberFormatter = new am4core.NumberFormatter();
    valueAxis.numberFormatter.numberFormat = "#. %";

    var interval;
    function startInterval() {
        interval = setInterval(function() {
            fetch('/api/home/cci/chart/'+ market_1 +'/'+ base_1 +'/'+ quote_1 +'/'+ market_2 +'/'+ base_2 +'/'+ quote_2 +'/1/'+ apiSecret +'/').then(
                function(response){
                    response.json().then(
                        function (dataNew) {
                            var toAdd = { date: dataNew[0]['date'], cci: dataNew[0]['cci'] }
                            chart.addData(toAdd, 1);
                        }
                    )
                }
            );
        }, 15*60 * 1000);
    }
    
    startInterval();

};


function fiatUpdate(delta) {
    let apiSecret = document.getElementById("APISecret").value;
    let htmlCards = document.getElementById("fiatPrices")
    function startInterval() {
        fiatInterval = setInterval(function() {
            fetch('/api/home/fiat-prices/'+ delta +'/'+ apiSecret +'/').then(
                function(response){
                    response.json().then(
                        function (dataNew) {
                            newHtmlPrices = ""
                            for (let line of dataNew){
                                let varColor = ''
                                let var2 = ''
                                if (line['change'] > 0) {
                                    varColor = 'success'
                                    var2 = 'trending_up'
                                }
                                else if (line['change'] < 0) {
                                    varColor = 'danger'
                                    var2 = 'trending_down'
                                }
                                else {
                                    varColor = 'warning'
                                    var2 = 'trending_flat'
                                }
                                newHtmlPrices += '<a href="charts/fiat/'+ line['symbol'] +'/" class="text-decoration-none"><div class="col p-1"><div class="p-1 border border-'+ varColor +' rounded-lg"><div class="row no-gutters align-items-center"><div class="col"><div class="text-center text-light"><strong>'+ line['symbol'] +'</strong></div><div class="text-center text-'+ varColor +'">'+ line['price'] +'</div></div><div class="col-auto"><div class="text-center text-light"><small><span class="material-icons text-'+ varColor +'">'+ var2 +'</span></small></div><div class="text-center text-'+ varColor +'"><small>'+ line['change'] +'%</small></div></div></div></div></div></a>'
                            }
                            htmlCards.innerHTML = newHtmlPrices
                        }
                    )
                }
            );
        }, 10 * 1000);
    }
    startInterval()
};
