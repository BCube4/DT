$(document).ready(function() {
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

    $('#searchBox').on('keypress', function(e) {
        if (e.which === 13) {
            e.preventDefault();
            $('#loadButton').click();
        }
    });

    $('#searchBox').on('focus input', function() {
        updateResults($(this).val().trim());
    });

    $(document).on('click', function(event) {
        if (!$(event.target).closest('#searchBox, #results').length) {
            $('#results').hide();
        }
    });

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

    $('#results').on('click', '.list-group-item-action', function() {
        var filename = $(this).text();
        $('#searchBox').val(filename);
        $('#results').hide();
    });

    $(window).on('resize', function() {
        // Ваша логика для обновления позиции элементов при изменении размера окна, если необходимо
    });
});
