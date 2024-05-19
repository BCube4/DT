$(document).ready(function() {
    var lastFilename = null;

    // Обработчик события для отображения ввода прогноза
    $(document).on('displayPredictionInputs', function(event, data) {
        lastFilename = data.filename;
        $('#predictionContainer').show();
    });

    // Обработчик нажатия на кнопку получения прогноза
    $('#getPredictionButton').click(function() {
        var days = parseInt($('#daysInput').val(), 10); // Преобразование в целое число
        if (!days || days <= 0) {
            alert('Введите корректное количество дней');
            return;
        }
        getPredictions(lastFilename, days);
    });

    // Обработчик нажатия клавиши Enter в поле ввода дней
    $('#daysInput').keypress(function(event) {
        if (event.which === 13) { // Проверка нажатия клавиши Enter
            $('#getPredictionButton').click();
        }
    });

    // Обработчик события для очистки данных
    $(document).on('clearData', function() {
        $('#predictionContainer').hide();
        $('#predictionTableContainer').hide();
    });

    // Функция для получения предсказаний
    function getPredictions(filename, days) {
        $.post('/analyze', { filename: filename, days_ahead: days }, function(response) {
            if (response.status === 'success') {
                generatePredictionTable(days, response.predictions);
            } else {
                alert('Ошибка при получении предсказаний');
            }
        }).fail(function() {
            alert('Ошибка соединения с сервером');
        });
    }

    // Функция для генерации таблицы предсказаний
    function generatePredictionTable(days, predictions) {
        var today = new Date();
        var predictionTableBody = $('#predictionTable tbody');
        predictionTableBody.empty();

        for (var i = 0; i < days; i++) {
            var predictionDate = new Date(today);
            predictionDate.setDate(today.getDate() + i + 1);
            var dateString = predictionDate.toLocaleDateString('ru-RU');

            if (predictions && predictions[i] !== undefined) {
                var predictedValue = predictions[i].toFixed(3);
                predictionTableBody.append(`<tr><td>${dateString}</td><td>${predictedValue}</td></tr>`);
            } else {
                predictionTableBody.append(`<tr><td>${dateString}</td><td>Нет данных</td></tr>`);
            }
        }

        var dayWord = declensionOfDays(days);
        $('#predictionTableTitle').text(`Прогноз на ${days} ${dayWord}`);
        $('#predictionTableContainer').show();

        // Анимация прокрутки
        $('html, body').animate({
            scrollTop: $('#predictionTableContainer').offset().top
        }, 1000);
    }

    // Функция для склонения слова "день" в зависимости от числа
    function declensionOfDays(days) {
        if (days % 10 === 1 && days % 100 !== 11) {
            return 'день';
        } else if ([2, 3, 4].includes(days % 10) && ![12, 13, 14].includes(days % 100)) {
            return 'дня';
        } else {
            return 'дней';
        }
    }
});
