
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

