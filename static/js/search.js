$(document).ready(function() {
    // Функция для обновления результатов поиска
    function updateResults(query) {
        $.post('/search', {query: query}, function(data) {
            $('#results').empty();
            if (data.length > 0) {
                data.forEach(function(file) {
                    $('#results').append(`<button type="button" class="list-group-item list-group-item-action">${file}</button>`);
                });
                $('#results').show();
            } else {
                $('#results').append('<div class="list-group-item" style="color: red;">Файл не найден</div>');
                $('#results').show();
            }
        }).fail(function() {
            $('#results').empty().append('<div class="list-group-item" style="color: red;">Ошибка загрузки</div>').show();
        });
    }

    // Обработчик для ввода в поисковую строку
    $('#searchBox').on('keypress', function(e) {
        if (e.which === 13) {  // Проверка на нажатие Enter
            e.preventDefault();
            $('#loadButton').click();  // Клик на кнопку загрузки
        }
    });

    // Обновление результатов при вводе в поисковую строку
    $('#searchBox').on('focus input', function() {
        updateResults($(this).val().trim());
    });

    // Скрытие результатов при клике вне области поиска
    $(document).on('click', function(event) {
        if (!$(event.target).closest('#searchBox, #results').length) {
            $('#results').hide();
        }
    });

    // Обработчик для кнопки загрузки
    $('#loadButton').on('click', function() {
        var filename = $('#searchBox').val().trim();
        if (!filename) {
            $('#status').text("Введите название файла").css('color', 'red');
            return;
        }
        $.post('/validate', {filename: filename}, function(data) {
            // Обновляем текст и цвет сообщения в зависимости от статуса ответа
            $('#status').text(data.message).css('color', data.status === 'success' ? 'green' : 'red');
        }).fail(function() {
            // Явное обновление стиля для ошибок сети или сервера
            $('#status').text("Ошибка сервера").css('color', 'red');
        });
        $('#results').hide();
    });

    // Обработчик для выбора файла из списка результатов
    $('#results').on('click', '.list-group-item-action', function() {
        var filename = $(this).text();
        $('#searchBox').val(filename);
        $('#results').hide();
    });

    // Обработчик для изменения размера окна
    $(window).on('resize', function() {
        // Логика для обновления позиции элементов при изменении размера окна, если необходимо
    });
});
