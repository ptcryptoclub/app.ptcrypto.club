function worldMap (divName) {
    /**
 * ---------------------------------------
 * This demo was created using amCharts 4.
 * 
 * For more information visit:
 * https://www.amcharts.com/
 * 
 * Documentation is available at:
 * https://www.amcharts.com/docs/v4/
 * ---------------------------------------
 */

// Themes begin
am4core.useTheme(am4themes_dark);
am4core.useTheme(am4themes_animated);
// Themes end

 // Create map instance
var chart = am4core.create(divName, am4maps.MapChart);

// Set map definition
chart.geodata = am4geodata_worldLow;

// Set projection
// chart.projection = new am4maps.projections.AlbersUsa();

// Create map polygon series
var polygonSeries = chart.series.push(new am4maps.MapPolygonSeries());

//Set min/max fill color for each area
polygonSeries.heatRules.push({
  property: "fill",
  target: polygonSeries.mapPolygons.template,
  min: chart.colors.getIndex(1).brighten(1),
  max: chart.colors.getIndex(1).brighten(-0.3)
});

// Make map load polygon data (state shapes and names) from GeoJSON
polygonSeries.useGeodata = true;

// Set heatmap values for each state
polygonSeries.data = [
  {
    id: "US",
    value: 4447100
  },
  {
    id: "GB",
    value: 626932
  },
  {
    id: "PT",
    value: 5130632
  },
  {
    id: "ES",
    value: 2673400
  },
  {
    id: "FR",
    value: 33871648
  },
  {
    id: "CA",
    value: 43012615
  },
  {
    id: "MX",
    value: 3405565
  },
  {
    id: "AF",
    value: 783600
  },
  {
    id: "AL",
    value: 15982378
  },
  {
    id: "AU",
    value: 8186453
  },
  {
    id: "AT",
    value: 1211537
  },
  {
    id: "CF",
    value: 1293953
  },
  {
    id: "CN",
    value: 12419293
  },
  {
    id: "EC",
    value: 6080485
  },
  {
    id: "EG",
    value: 2926324
  },
  {
    id: "ET",
    value: 2688418
  },
  {
    id: "IQ",
    value: 4041769
  },
  {
    id: "FI",
    value: 4468976
  },
  {
    id: "JP",
    value: 1274923
  },
  {
    id: "MZ",
    value: 5296486
  },
  {
    id: "NO",
    value: 6349097
  },
  {
    id: "RU",
    value: 9938444
  },
  {
    id: "BR",
    value: 4919479
  },
  {
    id: "ZM",
    value: 2844658
  },
  {
    id: "AO",
    value: 5595211
  },
  {
    id: "AM",
    value: 902195
  }
];

// Set up heat legend
let heatLegend = chart.createChild(am4maps.HeatLegend);
heatLegend.series = polygonSeries;
heatLegend.align = "right";
heatLegend.valign = "bottom";
heatLegend.width = am4core.percent(20);
heatLegend.marginRight = am4core.percent(4);
heatLegend.minValue = 0;
heatLegend.maxValue = 40000000;

// Set up custom heat map legend labels using axis ranges
var minRange = heatLegend.valueAxis.axisRanges.create();
minRange.value = heatLegend.minValue;
minRange.label.text = "Little";
var maxRange = heatLegend.valueAxis.axisRanges.create();
maxRange.value = heatLegend.maxValue;
maxRange.label.text = "A lot!";

// Blank out internal heat legend value axis labels
heatLegend.valueAxis.renderer.labels.template.adapter.add("text", function(labelText) {
  return "";
});

// Configure series tooltip
var polygonTemplate = polygonSeries.mapPolygons.template;
polygonTemplate.tooltipText = "{name}: {value}";
polygonTemplate.nonScalingStroke = true;
polygonTemplate.strokeWidth = 0.5;

// Create hover state and set alternative fill color
var hs = polygonTemplate.states.create("hover");
hs.properties.fill = am4core.color("#3c5bdc");
}