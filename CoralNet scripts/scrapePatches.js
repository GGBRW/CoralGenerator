// Script to execute on page: https://coralnet.ucsd.edu/source/about/
// (On that page > Inspect > Console > Paste code > Enter)

const species = [
  'Acropora cervicornis',
  'Acropora cervicornis',
  'Acropora digitifera',
  'Acropora palmata',
  'Acropora prolifera',
  'Acropora secale',
  'Acropora valenciennesi',
  'Agaricia speciosa',
  'Astraea favistella',
  'Astraea pulchra',
  'Montastraea curta',
  'Pleurocorallium niveum',
  'Crypthelia viridis',
  'Diploastrea heliopora',
  'Diploria labyrinthiformis',
  'Distichopora borealis',
  'Distichopora violacea',
  'Echinopora reflexa',
  'Favia fragum',
  'Gemmipora brassica',
  'Goniastrea favulus',
  'Goniastrea favulus',
  'Goniopora columna',
  'Heliopora coerulea',
  'Heliopora coerulea',
  'Herpetolithus crassus',
  'Leptoseris cailleti',
  'Leptoseris cucullata',
  'Leptoseris gardineri',
  'Acropora aspera',
  'Madrepora conigera',
  'Madrepora cuneata',
  'Madrepora cytherea',
  'Madrepora florida',
  'Acropora formosa',
  'Madrepora horrida',
  'Madrepora humilis',
  'Madrepora hyacinthus',
  'Madrepora robusta',
  'Madrepora spicifera',
  'Madrepora surculosa',
  'Acropora tenuis',
  'Madrepora valida',
  'Manopora caliculata',
  'Manopora capitata',
  'Manopora digitata',
  'Montipora lichen',
  'Manopora lichen',
  'Manopora nodosa',
  'Manopora scabricula',
  'Meandrina meandrites',
  'Merulina rigida',
  'Merulina rigida',
  'Millepora alcicornis',
  'Montipora danae',
  'Astraea curta',
  'Pavonia decussata',
  'Pavonia praetorta',
  'Pocillopora damicornis',
  'Pocillopora damicornis caespitosa',
  'Pocillopora damicornis',
  'Pocillopora damicornis',
  'Pocillopora damicornis',
  'Pocillopora grandis',
  'Pocillopora meandrina',
  'Pocillopora molokensis',
  'Pocillopora molokensis',
  'Porites lobata',
  'Porites monticulosa',
  'Psammocora columna',
  'Pseudodiploria strigosa',
  'Scolymia australis',
  'Sideropora mordax',
  'Stylaster alaskanus',
  'Stylaster brochi',
  'Stylaster sanguineus',
  'Stylaster verrillii',
  'Tubipora musica',
  'Seriatopora hystrix'
]

async function fetchPatchImages(formUrl) {

  const response = await fetch(formUrl);
  const responseText = await response.text();
  const parser = new DOMParser();
  const doc = parser.parseFromString(responseText, 'text/html');

  const patchLabelSelect = doc.querySelector('select[name="patch_label"]');
  const csrfToken = doc.querySelector('input[name="csrfmiddlewaretoken"]').value;
  const allResults = {};

  if (!patchLabelSelect) {
    console.error("No patch_label select element found");
    return;
  }

  for (let i = 0; i < patchLabelSelect.options.length; i++) {
    const option = patchLabelSelect.options[i];
    if (option.value === '') continue; // Skip the 'Any' option

    // Check if patch label contains a species name in my catalog
    const containsSpecies = species.some(speciesName => {
      return speciesName.toLowerCase().split(" ").every(name => option.text.toLowerCase().includes(name));
    });
    if(containsSpecies === false) continue;

    const formData = new URLSearchParams();
    formData.append('csrfmiddlewaretoken', csrfToken);
    formData.append('patch_label', option.value);
    formData.append('image_form_type', 'search'); 

    try {
      const response = await fetch(formUrl, {
        method: 'POST',
        body: formData,
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
          'X-CSRFToken': csrfToken
        }
      });

      if (!response.ok) {
        throw new Error(`Network response was not ok: ${response.statusText}`);
      }

      const responseText = await response.text();
      const parser = new DOMParser();
      const doc = parser.parseFromString(responseText, 'text/html');

      const contentContainer = doc.querySelector('#content-container');
      if (!contentContainer) {
        continue;
      }

      const thumbWrappers = contentContainer.querySelectorAll('.thumb_wrapper');
      console.log(option.text + ": " + thumbWrappers.length + " results")
      const titles = [];

      thumbWrappers.forEach(wrapper => {
        const img = wrapper.querySelector('a img');
        if (img && img.title) {
          titles.push(img.title);
        }
      });

      if(titles.length) allResults[option.text] = titles;
    } catch (error) {
      console.error(`Error fetching images for patch label: ${option.text}`, error);
    }
  }

  console.log(allResults);
  return { url: formUrl, results: allResults };
}

async function fetchPatchImagesForURL(url) {
    try {
      const response = await fetch(url);
      const responseText = await response.text();
      const parser = new DOMParser();
      const doc = parser.parseFromString(responseText, 'text/html');
  
      const patchLabelSelect = doc.querySelector('select[name="patch_label"]');
      const form = doc.getElementById('search-form');
      const csrfToken = doc.querySelector('input[name="csrfmiddlewaretoken"]').value;
      const results = {};
  
      for (let i = 0; i < patchLabelSelect.options.length; i++) {
        const option = patchLabelSelect.options[i];
        if (option.value === '') continue; // Skip 'Any' 
        const containsSpecies = species.some(speciesName => {
          return speciesName.toLowerCase().split(" ").every(name => option.text.toLowerCase().includes(name));
        });
        if(containsSpecies === false) continue;
  
        patchLabelSelect.selectedIndex = i;
        const patchLabel = option.text;
        console.log(`Fetching images for patch label: ${patchLabel} (${i + 1}/${patchLabelSelect.options.length}) at ${url}`);
  
        const formData = new FormData(form);
  
        const response = await fetch(form.action, {
          method: form.method,
          body: formData,
          headers: {
            'X-CSRFToken': csrfToken
          }
        });
        
        // Response
        const responseText = await response.text();
        const parser = new DOMParser();
        const doc = parser.parseFromString(responseText, 'text/html');
  
        const contentContainer = doc.querySelector('#content-container');
        const thumbWrappers = contentContainer.querySelectorAll('.thumb_wrapper');
        console.log(`Found ${thumbWrappers.length} images for patch label: ${patchLabel} at ${url}`)
  
        const titles = [];
  
        thumbWrappers.forEach(wrapper => {
          const img = wrapper.querySelector('a img');
          if (img && img.title) {
            titles.push(img.title);
          }
        });
  
        results[patchLabel] = titles;
        console.log(`Found ${titles.length} images for patch label: ${patchLabel} at ${url}`);
      }
  
      return { url, results };
    } catch (error) {
      console.error(`Error processing URL: ${url}`, error);
      return { url, results: {} };
    }
}

async function fetchAllPatchImages(urls) {
    const allResults = {};
  
    const fetchPromises = urls.map(url => fetchPatchImages(url));
  
    const results = await Promise.all(fetchPromises);
  
    results.forEach(({ url, results }) => {
      if(Object.keys(results).length > 0)
        allResults[url] = results;
    });
  
    console.log(allResults);
    return allResults;
  }

const sources = Array.from(document.querySelectorAll('.object_list li a'));
const urls = sources.map(x => x.href + 'browse/patches/');
  
fetchAllPatchImages(urls);
