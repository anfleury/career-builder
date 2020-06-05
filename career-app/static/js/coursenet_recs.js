var width = 1200,
    height = 800,
    wmax = width-20,
    hmax = height-20,
    squish = 2.5,
    radius = 3;

var svg = d3.select("#recs-svg")
    .append("svg")
    .attr("width", width)
    .attr("height", height);

var svgback = svg.append("g");
var svgfront = svg.append("g");
var svgpathnodes = svg.append("g");
var svgpath = svg.append("g");

d3.csv('../../static/edges_output.csv', function(myedges) {

  myedges.forEach(function(d) {
    d.x1 = +d.x1;
    d.x2 = +d.x2;
    d.y1 = +d.y1;
    d.y2 = +d.y2;
    d.width = +d.width;
  });

  svgpath.append("svg:defs").append("svg:marker")
    .attr("id", "triangle")
    .attr("refX", 6)
    .attr("refY", 6)
    .attr("markerWidth", 30)
    .attr("markerHeight", 30)
    .attr("markerUnits","userSpaceOnUse")
    .attr("orient", "auto")
    .append("path")
    .attr("d", "M 0 0 12 6 0 12 3 6")
    .style("fill", "#000000");

  var lines = svgpath.append("g") // add red lines
     .attr("class", "mylines")
      .selectAll(".lines")
    .data(myedges)
    .enter().append("line")
     .attr("x1", function (d) { return wmax/2 + d.x1*wmax/squish - 100; })
     .attr("x2", function (d) { return wmax/2 + d.x2*wmax/squish - 100; })
     .attr("y1", function (d) { return hmax/2 + d.y1*hmax/squish + 80; })
     .attr("y2", function (d) { return hmax/2 + d.y2*hmax/squish + 80; })
     .style("stroke", function(d) { return d.color; })
     .style("stroke-width", function(d) { return d.width; });

   var arrows = svgpath.append("g")  // add arrows
      .attr("class", "mylines")
       .selectAll(".lines")
     .data(myedges).enter().append("line")
      .attr("x1", function (d) { return wmax/2 + d.x1*wmax/squish - 100; })
      .attr("x2", function (d) { return wmax/2 + d.x2*wmax/squish - 100; })
      .attr("y1", function (d) { return hmax/2 + d.y1*hmax/squish + 80; })
      .attr("y2", function (d) { return hmax/2 + d.y2*hmax/squish + 80; })
      .attr("marker-end", "url(#triangle)")
      .style("opacity",1.0)
});

d3.csv("../../static/nodes_output.csv", function(mynodes) {

  mynodes.forEach(function(d) {
    d.x = +d.x;
    d.y = +d.y
    d.strength = +d.strength
    d.radius = +d.radius;
  });

   function color(mynodes) { return mynodes.strength; }
   var crange = d3.extent(mynodes, function(d) { return +d.strength; });
   var crange = [1, 12]
   var colorScale = d3.scaleSequential(d3.interpolateGnBu).domain([crange[0], crange[1]]);
   // Plasma, Inferno, Magma, Viridis, YlOrRd

   function radius(mynodes) { return mynodes.radius; }
   var radiusScale = d3.scaleLinear().domain([2, 4]).range([3, 8]);
   var outlineScale = d3.scaleLinear().domain([2, 4]).range([.1, 2]);

   var mytooltip = d3.select('#recs-svg').append("div")
       .attr("class", "tooltip")
       .style("opacity", 0);

   var mapLabel = svg.append("text")
       .attr("y", 120)
       .attr("x", 30)
       .style("font-family", "Quicksand")
       .style("font-size","16px")

   var dot = svgpathnodes.append("g")
      .attr("class", "dots")
       .selectAll(".dot")
      .data(mynodes)
       .enter().append("circle")
      .attr("class", "dot")
      .attr("r", function(d) { return radiusScale(radius(d)); })
      .attr("cx", function (d) { return wmax/2 + d.x*wmax/squish - 100; })
      .attr("cy", function (d) { return hmax/2 + d.y*hmax/squish + 80; })
      .style("fill", function(d) { return colorScale(color(d)+1); })
      .style("opacity",.9)
      .style("stroke",'#111111')
      .style("stroke-width", function(d) { return outlineScale(radius(d)); })
      .on("mouseover", function(d){
        mapLabel.text(d.title)
      })
      .on("mouseout", mouseout);

  function mouseover(d) {
      mapLabel.text(d.title)
      mytooltip.transition() //mytooltip
       .duration(0)
       .style("opacity", .9)
       .style("position", "absolute")
       .style("text-align", "center")
       .style("padding","3px")
       .style("font-family","Quicksand")
       .style("font-size", "12px")
       .style("background", "#eeeeee")
       .style("border", "0px")
       .style("border-radius", "8px")
       .style("pointer-events", "none");
       };

      function mouseout(d) {
        mapLabel.text("")
        mytooltip.transition()
         .duration(200)
         .style("opacity", 0);
      }

});
