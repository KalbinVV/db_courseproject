$(window).ready(function(){
    $.ajax({
        url: '/api/get_housings_rent_statistics',
        method: 'GET',
        data: {
            date_start: $('#date_start').val(),
            date_end: $('#date_end').val()
        },
        success: function(response) {
            var sum_data = [{
                values: response.parsed.sum_values,
                labels: response.parsed.names,
                type: 'pie'
            }]

            var avg_data = [{
                values: response.parsed.avg_values,
                labels: response.parsed.names,
                type: 'pie'
            }]

            var layout = {
                height: 600,
                width: 800,
            };

            Plotly.newPlot('sum_pie', sum_data, layout);
            Plotly.newPlot('avg_pie', avg_data, layout);
        }
    })
})