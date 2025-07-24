/*
 * Поиск файлов в папке Excel.
 */
$(document).ready(function() {
    function updateResults(query) {
        $.post('/search', { query: query }, function(data) {
            const results = $('#results');
            results.empty();
            if (data.length > 0) {
                data.forEach(function(file) {
                    results.append(`<button type="button" class="list-group-item list-group-item-action">${file}</button>`);
                });
                results.show();
            } else if (query) {
                results.append('<div class="list-group-item text-danger">Файл не найден</div>');
                results.show();
            } else {
                results.hide();
            }
        }).fail(function() {
            $('#results').empty().append('<div class="list-group-item text-danger">Ошибка загрузки</div>').show();
        });
    }

    $('#searchBox').on('input focus', function() {
        updateResults($(this).val().trim());
    });

    $(document).on('click', function(event) {
        if (!$(event.target).closest('#searchBox, #results').length) {
            $('#results').hide();
        }
    });

    $('#results').on('click', '.list-group-item-action', function() {
        const filename = $(this).text();
        $('#searchBox').val(filename);
        $('#results').hide();
    });
});
