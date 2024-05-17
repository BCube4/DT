$(document).ready(function() {
    $(document).on('displayFeatureImportances', function(event, data) {
        displayFeatureImportances(data.featureImportances);
    });

    function displayFeatureImportances(importances) {
        var sortedImportances = Object.entries(importances).sort((a, b) => b[1] - a[1]);
        var table = $('<table></table>').addClass('table table-scroll');
        var thead = $('<thead></thead>').append('<tr><th>Признак</th><th>Важность</th></tr>');
        var tbody = $('<tbody></tbody>');

        sortedImportances.forEach(item => {
            var color = interpolateColor(item[1], sortedImportances[sortedImportances.length - 1][1], sortedImportances[0][1]);
            tbody.append(`<tr><td>${item[0]}</td><td style="background-color: ${color};">${item[1].toFixed(3)}</td></tr>`);
        });

        table.append(thead).append(tbody);
        $('#coefficientsList').empty().append(table);

        // Добавляем класс для вертикальной прокрутки
        $('#coefficientsList').addClass('table-container');
    }

    function interpolateColor(value, min, max) {
        const redStart = 254, greenStart = 128, blueStart = 124; // #fe807c
        const redEnd = 124, greenEnd = 254, blueEnd = 128;       // #7cfe80

        var fraction = (value - min) / (max - min);
        var red, green, blue;

        if (fraction <= 0.5) { // From red to white
            red = redStart + Math.round((255 - redStart) * fraction * 2);
            green = greenStart + Math.round((255 - greenStart) * fraction * 2);
            blue = blueStart + Math.round((255 - blueStart) * fraction * 2);
        } else { // From white to green
            red = 255 - Math.round((255 - redEnd) * (fraction - 0.5) * 2);
            green = 255 - Math.round((255 - greenEnd) * (fraction - 0.5) * 2);
            blue = 255 - Math.round((255 - blueEnd) * (fraction - 0.5) * 2);
        }

        return `rgb(${red}, ${green}, ${blue})`;
    }
});
