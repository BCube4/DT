$(document).ready(function() {
    var lastFilename = null;

    $('#loadButton').click(function() {
        clearOldData();  // Очистка данных перед каждым запросом
        var filename = $('#searchBox').val().trim();
        if (!filename) {
            $('#regressionFormula').text('Введите название файла').css('color', 'red');
            $(document).trigger('analysisFailed');
            return;
        }

        $.post('/validate', { filename: filename }, function(response) {
            if (response.status === 'success') {
                lastFilename = filename;  // Сохраняем filename
                $.post('/analyze', { filename: filename }, function(response) {
                    displayRegressionFormula(response);
                    $(document).trigger('analysisSuccess', { filename: filename, response: response });
                }).fail(function() {
                    $('#regressionFormula').text('Ошибка анализа данных').css('color', 'red');
                    $(document).trigger('analysisFailed');
                });
            } else {
                $('#regressionFormula').text(response.message || 'Ошибка при обработке данных').css('color', 'red');
                $(document).trigger('analysisFailed');
            }
        }).fail(function() {
            $('#regressionFormula').text('Ошибка соединения с сервером').css('color', 'red');
            $(document).trigger('analysisFailed');
        });
    });

    function clearOldData() {
        $('#regressionFormula').empty().css('color', '');
        $('#predictionContainer').hide();
        $('#predictionTableContainer').hide();
        $(document).trigger('clearData');
    }

    function displayRegressionFormula(data) {
        if (!data || !data.coefficients) {
            console.error("Invalid or incomplete data received:", data);
            return;
        }
        var dependentVariableName = Object.keys(data.last_day_dependent_vars)[0];
        var independents = data.last_day_independent_vars;
        var coefficients = data.coefficients;
        var predictedValue = 0;
        var formula = `\\textbf{${dependentVariableName}} =`;

        Object.keys(independents).forEach(function(variable, index) {
            var coef = coefficients[variable].toFixed(3);
            var sign = coef >= 0 ? (index > 0 ? ' + ' : ' ') : ' - ';
            var absCoef = Math.abs(coef).toFixed(3);
            formula += `${sign}${absCoef} \\cdot \\textbf{${variable}}`;
            predictedValue += coefficients[variable] * independents[variable];
        });

        formula += ` = ${predictedValue.toFixed(3)}`;
        $('#regressionFormula').html(`$$${formula}$$`).css('color', 'black');
        $('#dataAnalysisContainers').show();
        MathJax.typesetPromise().then(function() {
            $('#regressionFormulaContainer').scrollTop(0); // Прокручиваем контейнер вверх
        }).catch(function(error) {
            console.log("MathJax processing error:", error);
        });

        $(document).trigger('displayGauge', {
            predictedValue: predictedValue,
            mean: data.mean,
            std_dev: data.std_dev
        });

        $(document).trigger('displayFeatureImportances', {
            featureImportances: data.feature_importances
        });

        // Триггер для отображения ввода прогноза и кнопки
        $(document).trigger('displayPredictionInputs', {
            predictions: data.predictions,
            filename: lastFilename
        });
    }
});
