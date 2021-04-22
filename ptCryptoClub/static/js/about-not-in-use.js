

function projectChart(divName) {


    // Themes begin
    am4core.useTheme(am4themes_dark);
    am4core.useTheme(am4themes_animated);
    // Themes end



    var chart = am4core.create(divName, am4plugins_forceDirected.ForceDirectedTree);
    var networkSeries = chart.series.push(new am4plugins_forceDirected.ForceDirectedSeries())

    chart.data = [
        {
            name: "ptcrypto.club",
            children: [
                {
                    name: "app",
                    children: [
                        {
                            name: "Markets",
                            children: [
                                { name: "kraken", value: 200 }
                            ]
                        },
                        {
                            name: "Cryptos",
                            children: [
                                { name: "BTC", value: 150 },
                                { name: "ETH", value: 150 }
                            ]
                        },
                        {
                            name: "Fiats",
                            value: 150
                        },
                        {
                            name: "CCI",
                            value: 150
                        },
                        {
                            name: "Charts",
                            children: [
                                { name: "Line", value: 150 },
                                { name: "OHLC", value: 150 },
                                { name: "VTP", value: 150 }
                            ]
                        },
                        {
                            name: "Portfolio",
                            children: [
                                { name: "Buy", value:150 },
                                { name: "Sell", value:150 }
                            ]
                        }
                    ]
                },
                {
                    name: "iam",
                    children: [
                        { name: "B1", value: 150 },
                        { name: "B2", value:150 }
                    ]
                }

            ]
        }
    ];

    networkSeries.dataFields.value = "value";
    networkSeries.dataFields.name = "name";
    networkSeries.dataFields.children = "children";
    networkSeries.nodes.template.tooltipText = "{name}:{value}";
    networkSeries.nodes.template.fillOpacity = 1;

    networkSeries.nodes.template.label.text = "{name}"
    networkSeries.fontSize = 10;

    networkSeries.links.template.strokeWidth = 3;

    var hoverState = networkSeries.links.template.states.create("hover");
    hoverState.properties.strokeWidth = 3;
    hoverState.properties.strokeOpacity = 1;

    networkSeries.nodes.template.events.on("over", function (event) {
        event.target.dataItem.childLinks.each(function (link) {
            link.isHover = true;
        })
        if (event.target.dataItem.parentLink) {
            event.target.dataItem.parentLink.isHover = true;
        }

    })

    networkSeries.nodes.template.events.on("out", function (event) {
        event.target.dataItem.childLinks.each(function (link) {
            link.isHover = false;
        })
        if (event.target.dataItem.parentLink) {
            event.target.dataItem.parentLink.isHover = false;
        }
    })

}
