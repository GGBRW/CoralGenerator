// Script to execute on page: https://coralnet.ucsd.edu/source/about/
// (On that page > Inspect > Console > Paste code > Enter)

async function fetchLabelsFromUrls() {
    const urlElements = document.querySelectorAll('.object_list li a');
    const urls = Array.from(urlElements).map(a => a.href);

    const labels = {};

    for (let i = 0; i < 50; ++i) {
        const url = urls[i] + 'labelset/';
        console.log(url);
        try {
            const response = await fetch(url);
            const html = await response.text();
            const parser = new DOMParser();
            const doc = parser.parseFromString(html, 'text/html');
            
            const sourceName = doc.querySelector('h2').innerText.trim();
            labels[sourceName] = Array.from(doc.querySelectorAll('#label-table .name')).map(x => x.innerText.trim())
        } catch (error) {
            console.error(`Error, ${url}:`, error);
        }
    }

    return labels;
}

fetchLabelsFromUrls().then(labels => {
    console.log('Final Labels:', labels);
});