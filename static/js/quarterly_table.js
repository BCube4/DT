$(document).ready(function() {
    $('#loadButton').click(function() {
        $('#status').empty(); // Очистка текста статуса
        $('#dataTable').empty(); // Очистка данных в таблице
        $('#tableTitle').empty(); // Очистка заголовка таблицы
        $('#tableContainer').hide(); // Скрытие контейнера таблицы, если он был видим

        var filename = $('#searchBox').val().trim();
        if (!filename) {
            $('#status').text("Введите название файла").css('color', 'red');
            return;
        }

        $.post('/validate', {filename: filename}, function(response) {
            if (response.status === 'success') {
                displayData(response.data);
                $('#status').text('Файл успешно загружен').css('color', 'green');
            } else {
                $('#status').text(response.message || 'Ошибка при обработке файла').css('color', 'red');
            }
        }).fail(function() {
            $('#status').text("Ошибка сервера").css('color', 'red');
        });
    });

    function displayData(data) {
        $('#dataTable').empty();
        $('#tableTitle').text("Данные за последние 31 день").append('<button id="toggleButton" class="btn btn-primary">Показать больше...</button>');

        let table = `<table class='table'><thead><tr><th></th>`;
        for (let i = 1; i <= 31; i++) {
            table += `<th>${i}</th>`;
        }
        table += `</tr></thead><tbody>`;

        let keys = Object.keys(data[0]);
        keys.forEach((key, index) => {
            let className = index >= 3 && index < keys.length - 1 ? 'hiddenRow' : '';
            table += buildRow(key, data, className);
            if (index == 2) { // После третьей строки
                table += `<tr id="ellipsisRow"><td colspan="32" style="text-align:center; font-size: 24px;">...</td></tr>`;
            }
        });

        table += `</tbody></table>`;
        $('#dataTable').html(table);
        $('#tableContainer').show();

        $('#toggleButton').click(function() {
            $('.hiddenRow').toggle();
            const isHidden = $('.hiddenRow').is(':visible');
            $('#ellipsisRow').toggle(!isHidden);  // Скрыть или показать троеточия
            $(this).text(isHidden ? 'Скрыть' : 'Показать больше...');
        });
    }

    function buildRow(key, data, className = '') {
    let rowClass = className.trim();
    let keyClass = '';

    if (independentVariables.includes(key)) {
        keyClass = 'independent-color';
    } else if (dependentVariables.includes(key)) {
        keyClass = 'dependent-color';
    }

    let row = `<tr class="${rowClass}"><td class="${keyClass}">${key}</td>`;
    for (let i = 0; i < 31; i++) {
        row += `<td>${data[i][key] || '0'}</td>`;
    }
    row += `</tr>`;
    return row;
}

});
