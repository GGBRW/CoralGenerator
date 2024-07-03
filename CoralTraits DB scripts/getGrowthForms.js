async function fetchInnerText(url) {
    try {
      const response = await fetch(url);
      const text = await response.text();
      const parser = new DOMParser();
      const doc = parser.parseFromString(text, 'text/html');
      const element = doc.querySelectorAll('.row .col-sm-2')[6];
      return element ? element.innerText : 'Element not found';
    } catch (error) {
      console.error('Error fetching URL:', url, error);
      return 'Error';
    }
  }
  
  growthForms = {};
  
  (async function() {
    for (const spec in specLab) {
        const url = "https://www.coraltraits.org/species/" + specLab[spec] + "/traits/183";
      const innerText = await fetchInnerText(url);
      console.log(`URL: ${url}\nInnerText: ${innerText}\n`);
        growthForms[spec] = innerText;
    }
  })();

for(let i in growthForms) {
    growthForms[i] = growthForms[i].trim().replace('\n\n            (cat)', '')
}