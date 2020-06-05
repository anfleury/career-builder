var width = 1200,
    height = 800,
    wmax = width-20,
    hmax = height-20,
    squish = 2.5,
    radius = 3;

var svg = d3.select("#main-svg")
    .append("svg")
    .attr("width", width)
    .attr("height", height);

var svgback = svg.append("g");
var svgfront = svg.append("g");

d3.csv('../../static/edges_orig_plot.csv', function(myedges) {

  myedges.forEach(function(d) {
    d.x1 = +d.x1;
    d.x2 = +d.x2;
    d.y1 = +d.y1;
    d.y2 = +d.y2;
    d.width = +d.width;
  });

  var lines = svgback.append("g")
     .attr("class", "mylines")
      .selectAll(".lines")
    .data(myedges).enter().append("line")
     .attr("x1", function (d) { return wmax/2 + d.x1*wmax/squish - 100; })
     .attr("x2", function (d) { return wmax/2 + d.x2*wmax/squish - 100; })
     .attr("y1", function (d) { return hmax/2 + d.y1*hmax/squish + 80; })
     .attr("y2", function (d) { return hmax/2 + d.y2*hmax/squish + 80; })
     .style("stroke", "#111111")
     .style("stroke-width", 0.1 )
     .style("opacity",.8)
});

d3.csv("../../static/nodes_orig_plot.csv", function(mynodes) {

  mynodes.forEach(function(d) {
    d.x = +d.x;
    d.y = +d.y
    d.strength = +d.strength;
  });

   function color(mynodes) { return mynodes.strength; }
   var crange = d3.extent(mynodes, function(d) {return +d.strength;});
   var crange = [1, 12]
   var colorScale = d3.scaleSequential(d3.interpolateGnBu).domain([crange[0], crange[1]]);
   // Plasma, Inferno, Magma, Viridis, YlOrRd

   var mytooltip = d3.select('#main-svg').append("div")
       .attr("class", "tooltip")
       .style("opacity", 0);

  var titletext = svg.append("text")
      .attr("y", 30)
      .attr("x", 400)
      .style("font-family", "Quicksand")
      .style("font-size","32px")

  titletext.text("Course Network")

   var mapLabel = svg.append("text")
       .attr("y", 120)
       .attr("x", 30)
       .style("font-family", "Quicksand")
       .style("font-size","16px")

   var dot = svgfront.append("g")
      .attr("class", "dots")
       .selectAll(".dot")
      .data(mynodes)
       .enter().append("circle")
      .attr("class", "dot")
      .attr("r", radius)
      .attr("cx", function (d) { return wmax/2 + d.x*wmax/squish - 100; })
      .attr("cy", function (d) { return hmax/2 + d.y*hmax/squish + 80; })
      .style("fill", function(d) { return colorScale(color(d)+1); })
      .style("stroke",'#111111')
      .style("stroke-width", .1)
      .on("mouseover", function(d){
        mapLabel.text(d.title)
      })
      .on("mouseout", mouseout);

  function mouseover(d) {
      mapLabel.text(d.title)
      mytooltip.transition() //mytooltip
       .duration(0)
       .style("opacity", .9)
       .text(d.title)
       //.style("left", d + "px")
       //.style("top", (d-28) + "px")
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

      var fullHeight = .5*height;
      var fullWidth = 100;

      var legMargin = { top: 20, bottom: 20, left: 5, right: 80 };
      var legWidth = fullWidth - legMargin.right;
      var legHeight = fullHeight - legMargin.top - legMargin.bottom;

      xleg = 1100
      yleg = 300
      var legSvg = svgfront.insert("svg","svg")
          .attr("id","legend")
          .attr('width', fullWidth)
          .attr('height', fullHeight)
          .attr("x", xleg)
          .attr("y", yleg)
          //.attr("transform", "translate(" + legMargin.left + "," + legMargin.top + ")");

      var legLabel = svgfront.insert("text", "svg")
          .attr("x", xleg)
          .attr("y", yleg)
          .style("font-size","12px")
      legLabel.text("Topic #")

      var gradient = legSvg.append("defs")
            .append('svg:linearGradient')
            .attr('id', 'gradient')
            .attr('x1', '0%') // bottom
            .attr('y1', '100%')
            .attr('x2', '0%') // to top
            .attr('y2', '0%')
            .attr('spreadMethod', 'pad');

      var linspace = function(start, stop, nsteps){
        delta = (stop-start)/(nsteps-1)
        return d3.range(start, stop+delta, delta).slice(0, nsteps)
      }

      var pct = linspace(0, 100, 12).map(function(d) {
          return Math.round(d);
      });

      var legrange = crange[1] - crange[0] + 1

      for (var i = 0; i < pct.length; i++) {
        gradient.append('stop')
            .attr('offset', pct[i] + '%')
            .attr('stop-color', colorScale(pct[i]/100*legrange+crange[0]))
            .attr('stop-opacity', 1);
          };

      legSvg.append('rect')
          .attr('x1', 0)
          .attr('y1', 0)
          .attr('width', legWidth)
          .attr('height', legHeight)
          .attr("transform", "translate(" + legMargin.left + "," + legMargin.top + ")")
          .style('fill', 'url(#gradient)');

      var legScale = d3.scaleLinear()
          .domain([crange[0], crange[1]])
          .range([legHeight, 0]);

      var legAxis = d3.axisRight()
          .scale(legScale);

      var legleftshift = +legWidth + +legMargin.left;

      legSvg.append("g")
          .attr("class", "legend axis")
          .attr("transform", "translate(" + legleftshift + "," + legMargin.top + ")")
          .call(legAxis)
          .attr("class","legformat")

});
