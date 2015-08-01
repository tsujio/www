var drawTraffic = function(traffic) {
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
    .domain([0, d3.max(traffic, function(d) { return d[1]; })])
    .range([h - padding, padding]);

  // Draw bars
  var widthPerDate = (w - padding * 2) / traffic.length;
  svg.selectAll("rect")
    .data(traffic)
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
    .data(traffic)
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
};

var drawReferer = function(referer) {
  // Draw table
  var table = d3.select('#referer').append('table');
  var thead = table.append('thead');
  var tbody = table.append('tbody');

  thead.append('tr')
    .selectAll('th')
    .data(['From', '#'])
    .enter()
    .append('th')
    .text(function(d) { return d; });

  tbody.selectAll('tr')
    .data(referer)
    .enter()
    .append('tr')
    .selectAll('td')
    .data(function(d) {
      return d3.entries(d);
    })
    .enter()
    .append('td')
    .text(function(d) { return d.value; })

  // Draw circle graph
  var w = 300;
  var h = 300;
  var padding = 10;

  var svg = d3.select("#referer")
    .append("svg")
    .attr("width", w)
    .attr("height", h)
    .append("g")
    .attr("transform", "translate(" + w / 2 + "," + h / 2 + ")");

  var arc = d3.svg.arc()
    .outerRadius((w - padding * 2) / 2);

  var pie = d3.layout.pie()
    .sort(null)
    .value(function(d){ return d[1]; });

  var g = svg.selectAll(".fan")
    .data(pie(referer))
    .enter()
    .append("g")
    .attr("class", "fan");

  var color = d3.scale.category20();

  g.append("path")
    .attr("d", arc)
    .attr("fill", function(d, i) {
      return color(i);
    });
};

$(function() {
  $.ajax('/cgi-bin/private/traffic.cgi', {
    dataType: 'json'
  }).done(function(data) {
    drawTraffic(data.traffic);
    drawReferer(data.referer);
  }).fail(function(jqXHR, textStatus) {
    alert(textStatus);
  });
});
