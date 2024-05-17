document.getElementById('loadButton').addEventListener('click', function() {
    const filename = document.getElementById('searchBox').value;
    fetch('/get_regression_coefficients', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: 'filename=' + encodeURIComponent(filename)
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            const formulaSection = document.getElementById('regressionFormula');
            let formula = `${data.dependent_var} = `;
            Object.keys(data.coefficients).forEach(varName => {
                formula += `${data.coefficients[varName].toFixed(2)} * ${varName} + `;
            });
            formula = formula.slice(0, -3); // Удаляем последний '+'
            formulaSection.innerHTML = `<p>Формула линейной регрессии: ${formula}</p>`;
            document.getElementById('regressionContainer').style.display = 'block';
        } else {
            alert('Ошибка: ' + data.message);
        }
    })
    .catch(error => console.error('Ошибка:', error));
});
