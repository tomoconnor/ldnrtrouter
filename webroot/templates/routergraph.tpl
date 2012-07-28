<!doctype html>
<head>
<script src="d3.min.js"></script>
<script src="d3.layout.min.js"></script>

<script src="rickshaw.min.js"></script>
<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.6.2/jquery.min.js"></script>
<script src="https://ajax.googleapis.com/ajax/libs/jqueryui/1.8.15/jquery-ui.min.js"></script>

	<link type="text/css" rel="stylesheet" href="http://jqueryui.com/themes/base/jquery.ui.all.css">
	<link type="text/css" rel="stylesheet" href="graph.css">
	<link type="text/css" rel="stylesheet" href="detail.css">
	<link type="text/css" rel="stylesheet" href="legend.css">
	<link type="text/css" rel="stylesheet" href="lines.css">
	<link type="text/css" rel="stylesheet" href="css/extensions.css">


	<script src="../src/js/Rickshaw.js"></script>
	<script src="../src/js/Rickshaw.Class.js"></script>
	<script src="../src/js/Rickshaw.Compat.ClassList.js"></script>
	<script src="../src/js/Rickshaw.Graph.js"></script>
	<script src="../src/js/Rickshaw.Graph.Renderer.js"></script>
	<script src="../src/js/Rickshaw.Graph.Renderer.Area.js"></script>
	<script src="../src/js/Rickshaw.Graph.Renderer.Line.js"></script>
	<script src="../src/js/Rickshaw.Graph.Renderer.Bar.js"></script>
	<script src="../src/js/Rickshaw.Graph.Renderer.ScatterPlot.js"></script>
	<script src="../src/js/Rickshaw.Graph.RangeSlider.js"></script>
	<script src="../src/js/Rickshaw.Graph.HoverDetail.js"></script>
	<script src="../src/js/Rickshaw.Graph.Annotate.js"></script>
	<script src="../src/js/Rickshaw.Graph.Legend.js"></script>
	<script src="../src/js/Rickshaw.Graph.Axis.Time.js"></script>
	<script src="../src/js/Rickshaw.Graph.Behavior.Series.Toggle.js"></script>
	<script src="../src/js/Rickshaw.Graph.Behavior.Series.Order.js"></script>
	<script src="../src/js/Rickshaw.Graph.Behavior.Series.Highlight.js"></script>
	<script src="../src/js/Rickshaw.Graph.Smoother.js"></script>
	<script src="../src/js/Rickshaw.Graph.Unstacker.js"></script>
	<script src="../src/js/Rickshaw.Fixtures.Time.js"></script>
	<script src="../src/js/Rickshaw.Fixtures.Number.js"></script>
	<script src="../src/js/Rickshaw.Fixtures.RandomData.js"></script>
	<script src="../src/js/Rickshaw.Fixtures.Color.js"></script>
	<script src="../src/js/Rickshaw.Color.Palette.js"></script>
	<script src="../src/js/Rickshaw.Graph.Axis.Y.js"></script>

	<script src="js/extensions.js"></script>


</head>
<body>
<div id="chart_container">
	<div id="chart"></div>
	<div id="legend_container">
		<div id="smoother" title="Smoothing"></div>
		<div id="legend"></div>
	</div>
	<div id="slider"></div>
</div>
<script>

var graph = new Rickshaw.Graph({
	element: document.querySelector("#chart"),
	width: 640,
	height: 480,
	renderer: 'line',
	series: [{
		data: [{{dataseries1}} ],
		color: '#4682b4',
		name: '{{dataseries1_name}}'
	}, {
		data: [ {{dataseries2}} ],
		color: '#9cc1e0',
		name: '{{dataseries2_name}}'
	}]
});
graph.render();
var hoverDetail = new Rickshaw.Graph.HoverDetail( {
    graph: graph,
    xFormatter: function(x) { return x + "seconds" },
    yFormatter: function(y) { return Math.floor(y / 1024.0) + " Kb/s" }
} );
var legend = new Rickshaw.Graph.Legend( {
	graph: graph,
	element: document.getElementById('legend')

} );

var shelving = new Rickshaw.Graph.Behavior.Series.Toggle( {
	graph: graph,
	legend: legend
} );

var axes = new Rickshaw.Graph.Axis.Time( {
	graph: graph
} );
axes.render();

</script>

</body>
