<!doctype html>
<script src="d3.min.js"></script>
<script src="d3.layout.min.js"></script>

<script src="rickshaw.min.js"></script>

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
		color: '#4682b4'
	}, {
		data: [ {{dataseries2}} ],
		color: '#9cc1e0'
	}]
});
graph.render();
var hoverDetail = new Rickshaw.Graph.HoverDetail( {
	graph: graph
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


