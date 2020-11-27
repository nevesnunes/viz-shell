/* global d3 */

var add = function(content) {
    const div = document.createElement('div');
    div.classList.add('columns');
    const divChild = document.createElement('div');
    divChild.classList.add('column');
    const size = 600;

    div.appendChild(divChild);
    const vizs = document.querySelector('#vizs');
    vizs.appendChild(div);

    const position = 4;
    const palette = d3.interpolateCividis;
    const rects = d3.select(divChild)
        .append('svg')
        .attr("shape-rendering", "crispEdges")
        .attr("width", `${size}`)
        .attr("height", `${size}`)
        .append("g")
        .selectAll("rect")
        .data(content.values);
    rects
        .enter()
        .append("rect")
        .merge(rects)
        .attr("x", d => d[0] * position)
        .attr("y", d => d[1] * position)
        .attr("width", position)
        .attr("height", position)
        .style("fill", d => palette(d[3]))
        .style("stroke", "black");
};

export {
    add
};
