/* global d3 */

// References:
// - https://bl.ocks.org/pstuffa/26363646c478b2028d36e7274cedefa6

var add = function(content) {
    const div = document.createElement('div');
    div.classList.add('columns');
    const divChild = document.createElement('div');
    divChild.classList.add('column');
    const size = 600;
    const margin = {
            top: size/20,
            right: size/20,
            bottom: size/20,
            left: size/20
        },
        width = size - margin.left - margin.right,
        height = size - margin.top - margin.bottom;

    div.appendChild(divChild);
    const vizs = document.querySelector('#vizs');
    vizs.appendChild(div);

    var dataset = content.values.map(function(d) {
        return {
            "x": d[0],
            "y": d[1]
        };
    });

    var xScale = d3.scaleLinear()
        .domain([content.min[0], content.max[0]])
        .range([0, width]);

    var yScale = d3.scaleLinear()
        .domain([content.min[1], content.max[1]])
        .range([height, 0]);

    var line = d3.line()
        .x(function(d) {
            return xScale(d.x);
        })
        .y(function(d) {
            return yScale(d.y);
        })
        .curve(d3.curveMonotoneX);

    var svg = d3.select(divChild)
        .append('svg')
        .attr("width", `${width + margin.left + margin.right}`)
        .attr("height", `${height + margin.top + margin.bottom}`)
        .append("g")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

    svg.append("g")
        .attr("class", "x axis")
        .attr("transform", "translate(0," + height + ")")
        .call(d3.axisBottom(xScale));
    svg.append("g")
        .attr("class", "y axis")
        .call(d3.axisLeft(yScale));

    svg.append("path")
        .datum(dataset)
        .attr("class", "line")
        .attr("d", line);

    svg.selectAll(".dot")
        .data(dataset)
        .enter().append("circle")
        .attr("class", "dot")
        .attr("cx", function(d) {
            return xScale(d.x)
        })
        .attr("cy", function(d) {
            return yScale(d.y)
        })
        .attr("r", 2);
};

export {
    add
};
