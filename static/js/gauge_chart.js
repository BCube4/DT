let ctx, centerX, centerY, radius, tickWidth;
let lastGaugeData = null;

document.addEventListener('DOMContentLoaded', function() {
    const canvas = document.getElementById('gaugeChart');
    if (!canvas) {
        console.error("Canvas element not found!");
        return;
    }

    ctx = canvas.getContext('2d');

    // Убедимся, что resizeCanvas вызывается после полной загрузки страницы
    window.addEventListener('resize', () => {
        requestAnimationFrame(resizeCanvas);
    });

    $(document).on('displayGauge', function(event, data) {
        if (typeof data.predictedValue !== 'number' || typeof data.mean !== 'number' || typeof data.std_dev !== 'number') {
            console.error("Invalid data received:", data);
            return;
        }
        lastGaugeData = data;
        drawGauge(data.predictedValue, data.mean, data.std_dev);
    });

    $(document).on('clearData', function() {
        console.log("Attempting to clear canvas with context:", ctx);
        clearCanvas();
        lastGaugeData = null;
    });

    // Убедимся, что resizeCanvas вызывается после полной загрузки страницы и всех элементов
    requestAnimationFrame(resizeCanvas);
});

function resizeCanvas() {
    const canvas = document.getElementById('gaugeChart');
    const parent = canvas.parentElement;
    const size = Math.min(parent.clientWidth, parent.clientHeight);
    canvas.width = size;
    canvas.height = size;
    centerX = canvas.width / 2;
    centerY = canvas.height / 2;
    radius = Math.min(centerX, centerY) * 0.8;
    tickWidth = radius * 0.1;

    if (lastGaugeData) {
        drawGauge(lastGaugeData.predictedValue, lastGaugeData.mean, lastGaugeData.std_dev);
    }
}

function drawGauge(predictedValue, mean, std_dev) {
    if (!ctx) {
        console.error("Context not provided!");
        return;
    }

    if (predictedValue === undefined || mean === undefined || std_dev === undefined) {
        console.error("Missing data for gauge rendering");
        return;
    }

    ctx.clearRect(0, 0, ctx.canvas.width, ctx.canvas.height);

    const colors = ["#ed1c24", "#fe807c", "#ffe87f", "#c2ff68", "#00ff00", "#00ff00", "#c2ff68", "#ffe87f", "#fe807c", "#ed1c24"];
    const angleOffset = -Math.PI / 2;
    const totalAngle = Math.PI;
    const rotateOffset = -Math.PI / 2;

    colors.forEach((color, index) => {
        const sliceAngle = totalAngle / colors.length;
        const startAngle = angleOffset + rotateOffset + index * sliceAngle;
        const endAngle = startAngle + sliceAngle;

        ctx.save();
        ctx.translate(centerX, centerY);
        ctx.beginPath();
        ctx.arc(0, 0, radius, startAngle, endAngle, false);
        ctx.lineWidth = tickWidth;
        ctx.strokeStyle = color;
        ctx.stroke();
        ctx.restore();
    });

    drawTicks(mean, std_dev, colors.length, angleOffset, totalAngle);
    drawLabels(mean, std_dev);
    drawPointer(predictedValue, mean, std_dev);
    drawValueAbove(mean);
    drawPredictedValueBelow(predictedValue);
}

function clearCanvas() {
    console.log("clearCanvas called with ctx:", ctx);
    if (!ctx) {
        console.error("Context not provided in clearCanvas");
        return;
    }
    ctx.clearRect(0, 0, ctx.canvas.width, ctx.canvas.height);
}

function drawTicks(mean, std_dev, numColors, angleOffset, totalAngle) {
    const sliceAngle = totalAngle / numColors;

    for (let i = 0; i <= numColors; i++) {
        const angle = angleOffset + i * sliceAngle;
        ctx.save();
        ctx.translate(centerX, centerY);
        ctx.rotate(angle);
        ctx.beginPath();
        ctx.moveTo(0, -radius);
        ctx.lineTo(0, -radius + tickWidth / 2);
        ctx.lineWidth = 2;
        ctx.strokeStyle = '#000';
        ctx.stroke();
        ctx.restore();
    }
}

function drawLabels(mean, std_dev) {
    ctx.textAlign = 'center';
    ctx.font = '16px Arial';
    ctx.fillStyle = 'black';

    const minPosX = centerX - radius - 30;
    const minPosY = centerY + 20;
    const maxPosX = centerX + radius + 30;
    const maxPosY = centerY + 20;

    ctx.fillText(`${(mean - std_dev).toFixed(1)}`, minPosX, minPosY);
    ctx.fillText(`${(mean + std_dev).toFixed(1)}`, maxPosX, maxPosY);
}

function drawPointer(predictedValue, mean, std_dev) {
    const minVal = mean - std_dev;
    const maxVal = mean + std_dev;
    const angle = valueToAngle(Number(predictedValue), minVal, maxVal);

    ctx.save();
    ctx.translate(centerX, centerY);
    ctx.rotate(angle);
    ctx.beginPath();
    ctx.moveTo(0, 0);
    ctx.lineTo(0, -radius + 20);
    ctx.lineWidth = 4;
    ctx.strokeStyle = 'black';
    ctx.stroke();
    ctx.restore();

    ctx.save();
    ctx.translate(centerX, centerY);
    ctx.beginPath();
    ctx.arc(0, 0, 5, 0, 2 * Math.PI);
    ctx.fillStyle = 'black';
    ctx.fill();
    ctx.restore();
}

function valueToAngle(value, min, max) {
    const minAngle = -Math.PI / 2;
    const maxAngle = Math.PI / 2;
    value = Math.max(min, Math.min(max, value));
    return (value - min) / (max - min) * (maxAngle - minAngle) + minAngle;
}

function drawValueAbove(mean) {
    ctx.fillStyle = 'black';
    ctx.textAlign = 'center';
    ctx.fillText(`${mean.toFixed(1)}`, centerX, centerY - radius - 20);
}

function drawPredictedValueBelow(predictedValue) {
    if (Number.isNaN(Number(predictedValue))) {
        console.error("Invalid predictedValue:", predictedValue);
        return;
    }
    ctx.fillStyle = 'black';
    ctx.textAlign = 'center';
    const offset = 30;
    ctx.fillText(`${Number(predictedValue).toFixed(1)}`, centerX, centerY + offset);
}
