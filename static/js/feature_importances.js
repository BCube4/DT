$(document).ready(function() {
    // Обработчик события для отображения важности признаков
    $(document).on('displayFeatureImportances', function(event, data) {
        displayFeatureImportances(data.featureImportances);
    });

    // Обработчик события для очистки данных
    $(document).on('clearData', function() {
        clearTable();
    });

    function displayFeatureImportances(importances) {
        var sortedImportances = Object.entries(importances).sort((a, b) => b[1] - a[1]);
        var tbody = $('#featureImportancesTable tbody');
        tbody.empty();

        sortedImportances.forEach(item => {
            var color = interpolateColor(item[1], sortedImportances[sortedImportances.length - 1][1], sortedImportances[0][1]);
            var row = $('<tr></tr>');
            row.append(`<td>${item[0]}</td>`);
            row.append(`<td style="background-color: ${color};">${item[1].toFixed(3)}</td>`);
            tbody.append(row);
        });

        // Удаление лишнего пространства сверху
        $('#coefficientsContainer').css('padding-top', '0');
    }

    function clearTable() {
        $('#featureImportancesTable tbody').empty();
    }

    function interpolateColor(value, min, max) {
        const redStart = 254, greenStart = 128, blueStart = 124; // #fe807c
        const redEnd = 124, greenEnd = 254, blueEnd = 128;       // #7cfe80

        var fraction = (value - min) / (max - min);
        var red, green, blue;

        if (fraction <= 0.5) { // От красного к белому
            red = redStart + Math.round((255 - redStart) * fraction * 2);
            green = greenStart + Math.round((255 - greenStart) * fraction * 2);
            blue = blueStart + Math.round((255 - blueStart) * fraction * 2);
        } else { // От белого к зеленому
            red = 255 - Math.round((255 - redEnd) * (fraction - 0.5) * 2);
            green = 255 - Math.round((255 - greenEnd) * (fraction - 0.5) * 2);
            blue = 255 - Math.round((255 - blueEnd) * (fraction - 0.5) * 2);
        }

        return `rgb(${red}, ${green}, ${blue})`;
    }
});
