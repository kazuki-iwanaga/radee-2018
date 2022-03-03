var updateDataDisplay = (newDataStr) => {
    for (let i = 1; i < 16; i++) {
        document.querySelector('div#data-child-' + i).textContent = document.querySelector('div#data-child-' + (i + 1)).textContent;
    }
    document.querySelector('div#data-child-16').textContent = newDataStr;
};