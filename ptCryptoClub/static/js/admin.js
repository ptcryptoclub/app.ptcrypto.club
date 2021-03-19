

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
    chart.dataSource.reloadFrequency = 60 * 1000;

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
}
