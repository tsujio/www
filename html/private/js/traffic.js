$(function() {
  $.ajax('/cgi-bin/private/traffic.cgi', {
    dataType: 'json'
  }).done(function(data) {
    var w = 800;
    var h = 300;
    var barPadding = 1;
    var padding = 30;

    // Setup svg area
    var svg = d3.select("#traffic")
      .append("svg")
      .attr("width", w)
      .attr("height", h);

    // Setup scale object
    var yScale = d3.scale.linear()
      .domain([0, d3.max(data.traffic, function(d) { return d[1]; })])
      .range([h - padding, padding]);

    // Draw bars
    var widthPerDate = (w - padding * 2) / data.traffic.length;
    svg.selectAll("rect")
      .data(data.traffic)
      .enter()
      .append("rect")
      .attr("x", function(d, i) {
        return i * widthPerDate + padding + barPadding;
      })
      .attr("y", function(d) {
        return yScale(d[1]);
      })
      .attr("width", widthPerDate - barPadding)
      .attr("height", function(d) {
        return h - padding - yScale(d[1]);
      })
      .attr("fill", "teal");

    // Draw date label on bars
    svg.selectAll("text")
      .data(data.traffic)
      .enter()
      .append("text")
      .text(function(d) {
        return d[0].endsWith("01") ? d[0] : "";
      })
      .attr("x", function(d, i) {
        return i * widthPerDate + padding + barPadding + widthPerDate / 2;
      })
      .attr("y", function(d) {
        return h - padding / 2;
      })
      .attr("text-anchor", "middle")
      .attr("font-family", "sans-serif")
      .attr("font-size", "11px")
      .attr("fill", "black");

    // Draw axis
    svg.append("g")
      .attr("class", "axis")
      .attr("transform", "translate(" + padding + ",0)")
      .call(d3.svg.axis()
            .scale(yScale)
            .orient("left")
            .ticks(5));
  }).fail(function(jqXHR, textStatus) {
    alert(textStatus);
  });
});
