var margin = {
        top: 10,
        right: 30,
        bottom: 30,
        left: 50
    },
    width = document.querySelector("#histogram").getBoundingClientRect().width - margin.left - margin.right,
    height = document.querySelector("#histogram").getBoundingClientRect().height - margin.top - margin.bottom;

var data = [];

var svg_histogram = d3.select("#histogram")
    .append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
    .append("g")
    .attr("transform",
        "translate(" + margin.left + "," + margin.top + ")");

var x_histogram = d3.scaleLinear()
    .domain([0, 1000])
    .range([0, width]);
svg_histogram.append("g")
    .attr("transform", "translate(0," + height + ")")
    .call(d3.axisBottom(x_histogram));

var histogram = d3.histogram()
    .value(function (d) {
        return d.voltage;
    }) // I need to give the vector of value
    .domain(x_histogram.domain()) // then the domain of the graphic
    .thresholds(x_histogram.ticks(100)); // then the numbers of bins

var y_histogram = d3.scaleLinear()
    .range([height, 0]);
var yAxis_histogram = svg_histogram.append("g");

function updateHistogram(newData) {
    Array.prototype.push.apply(data, newData);
    var bins = histogram(data);
    y_histogram.domain([0, d3.max(bins, (d) => {
        return d.length;
    })]);
    yAxis_histogram
        .call(d3.axisLeft(y_histogram));
    var rects = svg_histogram.selectAll(".rects")
        .data(bins);
    rects.enter()
        .append("rect") // Add a new rect for each new elements
        .merge(rects) // get the already existing elements as well
        .attr("class", "rects")
        .attr("x", 1)
        .attr("transform", function (d) {
            return "translate(" + x_histogram(d.x0) + "," + y_histogram(d.length) + ")";
        })
        .attr("width", function (d) {
            return x_histogram(d.x1) - x_histogram(d.x0) - 1;
        })
        .attr("height", function (d) {
            return height - y_histogram(d.length);
        })
        // .style("fill", "#c993ff");
        .style("fill", "#69b3a2");
    rects.exit()
        .remove();
}

function resetHistogram() {
    var bins = histogram([]);
    y_histogram.domain([0, d3.max(bins, (d) => {
        return d.length;
    })]);
    yAxis_histogram
        .call(d3.axisLeft(y_histogram));
    var rects = svg_histogram.selectAll(".rects")
        .data(bins);
    rects.enter()
        .append("rect") // Add a new rect for each new elements
        .merge(rects) // get the already existing elements as well
        .attr("class", "rects")
        .attr("x", 1)
        .attr("transform", function (d) {
            return "translate(" + x_histogram(d.x0) + "," + y_histogram(d.length) + ")";
        })
        .attr("width", function (d) {
            return x_histogram(d.x1) - x_histogram(d.x0) - 1;
        })
        .attr("height", function (d) {
            return height - y_histogram(d.length);
        })
        // .style("fill", "#c993ff");
        .style("fill", "#69b3a2");
    rects.exit()
        .remove();

    data = [];
}