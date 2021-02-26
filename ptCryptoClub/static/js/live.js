

function liveChart (divName, market, base, quote) {

    let apiSecret = document.getElementById("APISecret").value;



        // Themes begin
        am4core.useTheme(am4themes_dark);
        am4core.useTheme(am4themes_animated);
        // Themes end
        
        var chart = am4core.create(divName, am4charts.XYChart);
        chart.hiddenState.properties.opacity = 0;
        
        chart.padding(0, 0, 0, 0);
        
        chart.zoomOutButton.disabled = true;
        chart.dateFormatter.inputDateFormat = "yyyy-MM-dd HH:mm:ss";
        
        chart.dataSource.url = '/api/market/chart/live/'+ market +'/'+ base +'/'+ quote +'/100/'+ apiSecret +'/'
        chart.dataSource.load();
        chart.dataSource.parser = new am4core.JSONParser();

        chart.cursor = new am4charts.XYCursor();
        chart.cursor.behavior = "none";
        
        var dateAxis = chart.xAxes.push(new am4charts.DateAxis());
        dateAxis.renderer.grid.template.location = 0;
        dateAxis.renderer.minGridDistance = 80;
        dateAxis.dateFormats.setKey("hour", "h:mm:ss");
        dateAxis.periodChangeDateFormats.setKey("second", "h:mm");
        dateAxis.periodChangeDateFormats.setKey("minute", "h:mm");
        dateAxis.periodChangeDateFormats.setKey("hour", "h:mm");
        //dateAxis.renderer.inside = true;
        dateAxis.renderer.axisFills.template.disabled = true;
        dateAxis.renderer.ticks.template.disabled = true;
        dateAxis.renderer.fontSize = "0.75em"
        //dateAxis.cursorTooltipEnabled = false;
        
        var valueAxis = chart.yAxes.push(new am4charts.ValueAxis());
        valueAxis.tooltip.disabled = true;
        valueAxis.interpolationDuration = 500;
        valueAxis.rangeChangeDuration = 500;
        valueAxis.renderer.inside = true;
        valueAxis.renderer.minLabelPosition = 0.05;
        valueAxis.renderer.maxLabelPosition = 0.95;
        valueAxis.renderer.axisFills.template.disabled = true;
        valueAxis.renderer.ticks.template.disabled = true;
        valueAxis.renderer.fontSize = "0.75em"
        
        var series = chart.series.push(new am4charts.LineSeries());
        series.dataFields.dateX = "closetime";
        series.dataFields.valueY = "nTrans";
        series.interpolationDuration = 500;
        series.defaultState.transitionDuration = 0;
        series.tensionX = 0.8;
        series.tooltipText = "Transactions: {valueY.value}";
        series.tooltip.getFillFromObject = false;
        series.tooltip.label.propertyFields.fill = am4core.color("#67b7dc");
        
        chart.events.on("datavalidated", function () {
            dateAxis.zoom({ start: 1 / 15, end: 1.2 }, false, true);
        });
        
        dateAxis.interpolationDuration = 500;
        dateAxis.rangeChangeDuration = 500;
        
        document.addEventListener("visibilitychange", function() {
            if (document.hidden) {
                if (interval) {
                    clearInterval(interval);
                }
            }
            else {
                startInterval();
            }
        }, false);
        
        // add data
        var interval;
        function startInterval() {
            interval = setInterval(function() {
                fetch('/api/market/chart/live/'+ market +'/'+ base +'/'+ quote +'/1/'+ apiSecret +'/').then(
                    function(response){
                        response.json().then(
                            function (dataNew) {
                                var toAdd = { closetime: dataNew[0]['closetime'], nTrans: dataNew[0]['nTrans'] }
                                chart.addData(toAdd, 1);
                            }
                        )
                    }
                );
            }, 20 * 1000);
        }
        
        startInterval();
        
        // all the below is optional, makes some fancy effects
        // gradient fill of the series
        series.fillOpacity = 1;
        var gradient = new am4core.LinearGradient();
        gradient.addColor(chart.colors.getIndex(0), 0.2);
        gradient.addColor(chart.colors.getIndex(0), 0);
        series.fill = gradient;
        
        // this makes date axis labels to fade out
        dateAxis.renderer.labels.template.adapter.add("fillOpacity", function (fillOpacity, target) {
            var dataItem = target.dataItem;
            return dataItem.position;
        })
        
        // need to set this, otherwise fillOpacity is not changed and not set
        dateAxis.events.on("validated", function () {
            am4core.iter.each(dateAxis.renderer.labels.iterator(), function (label) {
                label.fillOpacity = label.fillOpacity;
            })
        })
        

        
        // bullet at the front of the line
        var bullet = series.createChild(am4charts.CircleBullet);
        bullet.circle.radius = 5;
        bullet.fillOpacity = 1;
        bullet.fill = chart.colors.getIndex(0);
        bullet.isMeasured = false;
        
        series.events.on("validated", function() {
            bullet.moveTo(series.dataItems.last.point);
            bullet.validatePosition();
        });
        
}
