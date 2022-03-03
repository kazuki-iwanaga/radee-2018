const stateHandler = (event) => {
    switch (JSON.parse(event.data).state) {
        case 'standby':
            window.alert('現在、測定は行われていません。\n「実験名」と「測定時間」を入力して測定を始めましょう。\nちなみに、ページ中盤にマニュアルがあります。');
            resetHandler();
            break;

        case 'working':
            window.alert('現在、実験「' + JSON.parse(event.data).detail.name + '」が行われています。');
            startButton.disabled = true;
            downloadButton.disabled = true;
            resetButton.disabled = true;
            document.querySelector('input#project-name').value = JSON.parse(event.data).detail.name;
            document.querySelector('select').value = JSON.parse(event.data).detail.time;
            // console.log(JSON.parse(event.data).detail.time);
            document.querySelector('input#csv-name').value = '';
            break;

        case 'done':
            window.alert('実験「' + JSON.parse(event.data).detail.name + '」が終了しました。\nCSVファイルをダウンロードして保存してください。\n次の実験を行う際には「リセット」ボタンを押してください。');
            startButton.disabled = true;
            downloadButton.disabled = false;
            resetButton.disabled = false;
            document.querySelector('input#project-name').value = JSON.parse(event.data).detail.name;
            document.querySelector('select').value = JSON.parse(event.data).detail.time;
            document.querySelector('input#csv-name').value = 'http://localhost:3000/csv/' + JSON.parse(event.data).detail.name + '.csv';
            break;

        default:
            break;
    }
};

const reloadHandler = (event) => {
    var newDataArray = JSON.parse(event.data).data;
    updateHistogram(newDataArray);
    // console.log(newDataArray);
    if (newDataArray[newDataArray.length - 1]) {
        document.querySelector('input#now-time').value = newDataArray[newDataArray.length - 1].delta_t;
        document.querySelector('input#now-count').value = newDataArray.length;
    }
};

const newHandler = (event) => {
    var newDataArray = JSON.parse(event.data).data;
    updateHistogram(newDataArray);
    updateDataDisplay(`${newDataArray[0].datetime} , ${newDataArray[0].voltage}`);
    document.querySelector('input#now-time').value = newDataArray[0].delta_t;
    document.querySelector('input#now-count').value = data.length;
};

const startedHandler = (event) => {
    startButton.disabled = true;
    document.querySelector('input#project-name').value = JSON.parse(event.data).name;
    document.querySelector('select').value = JSON.parse(event.data).time;
    // console.log(JSON.stringify(event.data));
};

const finishHandler = () => {
    window.alert('測定が終了しました。\nCSVファイルをダウンロードしてください。');
    document.querySelector('input#csv-name').value = document.querySelector('input#project-name').value +
        '.csv';
    downloadButton.disabled = false;
    resetButton.disabled = false;
};

const resetHandler = () => {
    startButton.disabled = false;
    downloadButton.disabled = true;
    resetButton.disabled = true;
    for (let j = 1; j < 17; j++) {
        document.querySelector('div#data-child-' + j).textContent = '-------------------';
    }
    document.querySelector('input#now-time').value = '';
    document.querySelector('input#now-count').value = '';
    resetHistogram();
    document.querySelector('input#project-name').value = '';
    document.querySelector('input#csv-name').value = '';
    document.querySelector('select').value = '';
};
