

function adminLastUpdate(){
    let apiSecret = document.getElementById("APISecret").value;
    fetch('/api/admin/live-data/'+ apiSecret +'/').then(
        function(response){
            response.json().then(
                function (data) {
                    for (let line of data) {
                        let element = document.getElementById(line['market']+ '-' + line['base']+ '-' + line['quote'])
                        element.innerHTML = "<td>"+ line['market'] +"</td><td>"+ line['base'].toUpperCase() +"</td><td>"+ line['quote'].toUpperCase() +"</td><td>"+ line['date'] +"</td>"
                        if (line['all_good']){
                            element.className = "text-success"
                        }
                        else {
                            element.className = "text-danger"
                        }
                    }
                }
            )
        }
    );
};

function adminApiUsage(divName){
    let apiSecret = document.getElementById("APISecret").value;

    // Themes begin
    am4core.useTheme(am4themes_dark);
    am4core.useTheme(am4themes_animated);
    // Themes end

    // Create chart instance
    var chart = am4core.create(divName, am4charts.XYChart);
    chart.zoomOutButton.disabled = true;
    chart.dateFormatter.inputDateFormat = "yyyy-MM-dd HH:mm:ss";
    

    // Add data
    chart.dataSource.url = '/api/admin/api-usage/' + apiSecret + '/';
    chart.dataSource.load();
    chart.dataSource.keepCount = true;
    chart.dataSource.parser = new am4core.JSONParser();
    chart.dataSource.updateCurrentData = true;
    chart.dataSource.reloadFrequency = 30 * 1000;

    // Create axes
    var dateAxis = chart.xAxes.push(new am4charts.DateAxis());
    dateAxis.renderer.fontSize = "0.7em";
    dateAxis.renderer.grid.template.disabled = true;
    //dateAxis.tooltip.disabled = true;

    var valueAxis = chart.yAxes.push(new am4charts.ValueAxis());
    valueAxis.renderer.fontSize = "0.7em";
    valueAxis.renderer.grid.template.disabled = true;
    valueAxis.tooltip.disabled = true;

    // Create series
    var series = chart.series.push(new am4charts.ColumnSeries());
    series.dataFields.valueY = "usage";
    series.dataFields.dateX = "date";
    series.strokeWidth = 2;
    series.minBulletDistance = 10;
    series.tooltipText = "{valueY}";
    series.tooltip.pointerOrientation = "vertical";
    series.tooltip.background.cornerRadius = 2;
    series.tooltip.background.fillOpacity = 0.7;
    series.tooltip.label.padding(5,10,5,10)


    // Add cursor
    chart.cursor = new am4charts.XYCursor();
    chart.cursor.snapToSeries = series;
    chart.cursor.behavior = "none";
};

function adminApiUsageDetails(){
    let apiSecret = document.getElementById("APISecret").value;
    let elementTotal = document.getElementById('total');
    let element30days = document.getElementById('30days');
    let element7days = document.getElementById('7days');
    let element24h = document.getElementById('24h');
    fetch('/api/admin/api-usage/details/'+ apiSecret +'/').then(
        function(response){
            response.json().then(
                function (data) {
                    elementTotal.innerHTML = '<div class="border border-info rounded-lg p-2"><div class="text-left text-muted ml-3 mt-2"><h4><strong>Total</strong></h4></div><div class="text-right text-light"><h3><strong>'+ numberFormat(data['total']) +'</strong></h3></div><div class="small"><div class="row justify-content-between text-muted"><div class="col-auto">Users:</div><div class="col-auto">'+ numberFormat(data['total_users']) +'</div></div><div class="row justify-content-between text-muted"><div class="col-auto">Non users:</div><div class="col-auto">'+ numberFormat(data['total_n_users']) +'</div></div></div></div>'
                    element30days.innerHTML = '<div class="border border-info rounded-lg p-2"><div class="text-left text-muted ml-3 mt-2"><h4><strong>Last 30 days</strong></h4></div><div class="text-right text-light"><h3><strong>'+ numberFormat(data['last_month']) +'</strong></h3></div><div class="small"><div class="row justify-content-between text-muted"><div class="col-auto">Users:</div><div class="col-auto">'+ numberFormat(data['last_month_users']) +'</div></div><div class="row justify-content-between text-muted"><div class="col-auto">Non users:</div><div class="col-auto">'+ numberFormat(data['last_month_n_users']) +'</div></div></div></div>'
                    element7days.innerHTML = '<div class="border border-info rounded-lg p-2"><div class="text-left text-muted ml-3 mt-2"><h4><strong>Last 7 days</strong></h4></div><div class="text-right text-light"><h3><strong>'+ numberFormat(data['last_week']) +'</strong></h3></div><div class="small"><div class="row justify-content-between text-muted"><div class="col-auto">Users:</div><div class="col-auto">'+ numberFormat(data['last_week_users']) +'</div></div><div class="row justify-content-between text-muted"><div class="col-auto">Non users:</div><div class="col-auto">'+ numberFormat(data['last_week_n_users']) +'</div></div></div></div>'
                    element24h.innerHTML = '<div class="border border-info rounded-lg p-2"><div class="text-left text-muted ml-3 mt-2"><h4><strong>Last 24h</strong></h4></div><div class="text-right text-light"><h3><strong>'+ numberFormat(data['last_24h']) +'</strong></h3></div><div class="small"><div class="row justify-content-between text-muted"><div class="col-auto">Users:</div><div class="col-auto">'+ numberFormat(data['last_24h_users']) +'</div></div><div class="row justify-content-between text-muted"><div class="col-auto">Non users:</div><div class="col-auto">'+ numberFormat(data['last_24h_n_users']) +'</div></div></div></div>'
                }
            )
        }
    );
};

function adminApiUsageTop5(){
    let apiSecret = document.getElementById("APISecret").value;
    let notUserId = document.getElementById("notUser").value;
    let htmlTop5 = document.getElementById("top_5")
    fetch('/api/admin/api-usage/top-5/'+ apiSecret +'/').then(
        function(response){
            response.json().then(
                function (data) {
                    let notUserClass = ''
                    let linesHTML = '';
                    for (let line of data) {
                        if (line['user_id'] == notUserId) {
                            notUserClass = 'text-warning'
                        }
                        else {
                            notUserClass = 'text-muted'
                        }
                        linesHTML += '<tr class="'+ notUserClass +'"><td class="text-center">'+ numberFormat(line['user_id']) +'</td><td class="text-right">'+ numberFormat(line['usage']) +'</td></tr>'
                    }
                    htmlTop5.innerHTML = linesHTML
                }
            )
        }
    );
}


function adminCpuUsageWS(divName){
    let apiSecret = document.getElementById("APISecret").value;

    // Themes begin
    am4core.useTheme(am4themes_dark);
    am4core.useTheme(am4themes_animated);
    // Themes end
    
    var chart = am4core.create(divName, am4charts.XYChart);
    chart.hiddenState.properties.opacity = 0;
    
    chart.padding(0, 0, 0, 0);
    
    chart.zoomOutButton.disabled = false;
    chart.dateFormatter.inputDateFormat = "yyyy-MM-dd HH:mm:ss";
    chart.dataSource.url = '/api/admin/cpu-usage/webserver/'+ apiSecret +'/'
    chart.dataSource.load();
    chart.dataSource.parser = new am4core.JSONParser();

    chart.cursor = new am4charts.XYCursor();
    // chart.cursor.behavior = "none";
    
    var dateAxis = chart.xAxes.push(new am4charts.DateAxis());
    dateAxis.renderer.fontSize = "0.75em";
    dateAxis.tooltip.disabled = false;
    dateAxis.renderer.grid.template.disabled = true;
    

    var valueAxis = chart.yAxes.push(new am4charts.ValueAxis());
    valueAxis.tooltip.disabled = true;
    valueAxis.renderer.inside = true;
    valueAxis.renderer.minLabelPosition = 0.05;
    valueAxis.renderer.maxLabelPosition = 0.95;
    valueAxis.renderer.axisFills.template.disabled = true;
    valueAxis.renderer.ticks.template.disabled = true;
    valueAxis.renderer.fontSize = "0.75em"
    valueAxis.renderer.grid.template.disabled = true;
    valueAxis.title.text = "CPU usage (%)";
    valueAxis.title.fontSize = "0.75em"
    
    var series = chart.series.push(new am4charts.LineSeries());
    series.dataFields.dateX = "date";
    series.dataFields.valueY = "avg";
    series.tooltipText = "avg: {valueY.value}";

    var series2 = chart.series.push(new am4charts.LineSeries());
    series2.dataFields.dateX = "date";
    series2.dataFields.valueY = "max";
    series2.tooltipText = "max: {valueY.value}";
    series2.fill = am4core.color("red");
    series2.stroke = am4core.color("red");

    var series3 = chart.series.push(new am4charts.LineSeries());
    series3.dataFields.dateX = "date";
    series3.dataFields.valueY = "min";
    series3.tooltipText = "min: {valueY.value}";
    series3.fill = am4core.color("green");
    series3.stroke = am4core.color("green");

}

function adminCpuUsageDC(divName){
    let apiSecret = document.getElementById("APISecret").value;

    // Themes begin
    am4core.useTheme(am4themes_dark);
    am4core.useTheme(am4themes_animated);
    // Themes end
    
    var chart = am4core.create(divName, am4charts.XYChart);
    chart.hiddenState.properties.opacity = 0;
    
    chart.padding(0, 0, 0, 0);
    
    chart.zoomOutButton.disabled = false;
    chart.dateFormatter.inputDateFormat = "yyyy-MM-dd HH:mm:ss";
    chart.dataSource.url = '/api/admin/cpu-usage/data-creator/'+ apiSecret +'/'
    chart.dataSource.load();
    chart.dataSource.parser = new am4core.JSONParser();

    chart.cursor = new am4charts.XYCursor();
    // chart.cursor.behavior = "none";
    
    var dateAxis = chart.xAxes.push(new am4charts.DateAxis());
    dateAxis.renderer.fontSize = "0.75em";
    dateAxis.tooltip.disabled = false;
    dateAxis.renderer.grid.template.disabled = true;
    

    var valueAxis = chart.yAxes.push(new am4charts.ValueAxis());
    valueAxis.tooltip.disabled = true;
    valueAxis.renderer.inside = true;
    valueAxis.renderer.minLabelPosition = 0.05;
    valueAxis.renderer.maxLabelPosition = 0.95;
    valueAxis.renderer.axisFills.template.disabled = true;
    valueAxis.renderer.ticks.template.disabled = true;
    valueAxis.renderer.fontSize = "0.75em"
    valueAxis.renderer.grid.template.disabled = true;
    valueAxis.title.text = "CPU usage (%)";
    valueAxis.title.fontSize = "0.75em"
    
    var series = chart.series.push(new am4charts.LineSeries());
    series.dataFields.dateX = "date";
    series.dataFields.valueY = "avg";
    series.tooltipText = "avg: {valueY.value}";

    var series2 = chart.series.push(new am4charts.LineSeries());
    series2.dataFields.dateX = "date";
    series2.dataFields.valueY = "max";
    series2.tooltipText = "max: {valueY.value}";
    series2.fill = am4core.color("red");
    series2.stroke = am4core.color("red");

    var series3 = chart.series.push(new am4charts.LineSeries());
    series3.dataFields.dateX = "date";
    series3.dataFields.valueY = "min";
    series3.tooltipText = "min: {valueY.value}";
    series3.fill = am4core.color("green");
    series3.stroke = am4core.color("green");
    // series.tooltipText = "1 EUR = {valueY.value} "+fiat.toUpperCase();
    // series.fillOpacity = 0.2;

}
