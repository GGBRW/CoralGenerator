const puppeteer = require('puppeteer');
const https = require('https');
const fs = require('fs');

function downloadFile(fileUrl, outputPath) {
    const file = fs.createWriteStream(outputPath);
    https.get(fileUrl, (response) => {
        response.pipe(file);

        file.on('finish', () => {
            file.close();
            console.log('Download Completed');
        });
    }).on('error', (err) => {
        fs.unlink(outputPath); // Delete the file async. (But we don't check the result)
        console.error('Error downloading the file:', err.message);
    });
}


async function downloadObj(url) {
    const browser = await puppeteer.launch();
    const page = await browser.newPage();
    await page.goto(url);

    // Click the download button
    await page.click('#heading-tab-download');

    // Wait for the popover to appear
    await page.waitForSelector('.popover-body');

    // Extract the desired info
    const downloads = await page.evaluate(() => {
        function extractDetailsToJson(document) {
            const wrapper = document.querySelector('#edanWrapper');
            const dls = wrapper.querySelectorAll('dl');
            const details = {};
        
            dls.forEach(dl => {
                Array.from(dl.children).forEach(child => {
                    if (child.tagName === 'DT') {
                        // Ensure every DT starts with an empty array to accumulate DDs
                        const dtText = child.textContent.trim();
                        details[dtText] = details[dtText] || [];
                    } else if (child.tagName === 'DD') {
                        // Get the last DT key added to details
                        const lastDtKey = Object.keys(details)[Object.keys(details).length - 1];
                        const value = child.querySelector('a') ? child.querySelector('a').href : child.textContent.trim();
                        // Add the DD value to the array of the last DT key
                        details[lastDtKey].push(value);
                    }
                });
            });
        
            // Simplify entries with single DD to just a string, not an array
            Object.keys(details).forEach(key => {
                if (details[key].length === 1) {
                    details[key] = details[key][0];
                }
            });
        
            return details
        }

        let link;
        document.querySelectorAll('.popover-body li a').forEach(item => {
            if (item.innerText.includes('obj') && item.innerText.includes('Low Resolution')) {
                link = item.href; // or item.querySelector('a').href to get the download link
            }
        });
        return {
            title: document.querySelector('h1').innerText,
            link: link,
            data: extractDetailsToJson(document)
        }
    });

    const filename = downloads.link.split('/').pop();
    metadata[downloads.title] = {file: filename, metadata: downloads.data};
    downloadFile(downloads.link, 'smithsonian_corals/' + filename);
    await browser.close();
}

const links = JSON.parse(`["https://3d.si.edu/object/3d/acropora-cervicornis:dd875177-c986-48e2-9468-8e58f01099d3","https://3d.si.edu/object/3d/acropora-cervicornis:31d1de41-2c76-46bd-8484-afb32e969431","https://3d.si.edu/object/3d/acropora-digitifera:bfcdeb60-2d75-4a04-8d16-52f216b33351","https://3d.si.edu/object/3d/acropora-palmata:6fd30c79-3345-4d06-b27c-99d5b320ce5f","https://3d.si.edu/object/3d/acropora-prolifera:0124ceca-2430-4b1c-b5e0-3f9ba32815fe","https://3d.si.edu/object/3d/acropora-secale:cb2e1f4d-8eaa-454b-b61d-cc78b6b64b7b","https://3d.si.edu/object/3d/acropora-valenciennesi:ce579ce4-d647-47dc-a111-ccc931760d0b","https://3d.si.edu/object/3d/agaricia-speciosa:04fb6721-4c44-4526-8511-edd4adfc7c54","https://3d.si.edu/object/3d/astraea-flavistella:39444ca1-a8ca-47d4-926d-eb0c0e2dba63","https://3d.si.edu/object/3d/astraea-pulchra:5395c5bf-da23-4325-8ae8-f84c6d90a075","https://3d.si.edu/object/3d/astraea-coronata:481ab320-951f-4dac-9a7f-a5d8f1f558eb","https://3d.si.edu/object/3d/carcharhinus-altimus:d490078d-f538-4bbc-ba7f-977dcd69cd86","https://3d.si.edu/object/3d/corallium-sp:7fd1cb15-599b-44e5-8a14-579dfb749434","https://3d.si.edu/object/3d/crypthelia-viridis:0ec0d8c6-3474-4f2c-b5f5-323534d7b16d","https://3d.si.edu/object/3d/cypraecassis-rufa:8cd81303-17b2-413e-8804-93810f80b5a8","https://3d.si.edu/object/3d/diodon-hystrix:e0bdb234-d604-41fd-8f47-27368159c476","https://3d.si.edu/object/3d/diploastrea-heliopora:4876620d-4fc8-4d36-af06-bcfd2fab78be","https://3d.si.edu/object/3d/diploria-labyrinthiformis:87738412-3acd-45d1-bff4-3ab67093470e","https://3d.si.edu/object/3d/distichopora-borealis:09bf7376-fdc1-4693-bccd-80e90754d7f5","https://3d.si.edu/object/3d/distichopora-violacea:14ebe2e4-c7e3-4faa-aafe-d4f29e06c5de","https://3d.si.edu/object/3d/echinopora-reflexa:9922a8a1-e0bd-4c72-8511-aaf633ef6c2f","https://3d.si.edu/object/3d/favia-fragum:9d321ebb-d9d2-4812-829f-c74bd2565634","https://3d.si.edu/object/3d/gemmipora-brassica:dc07b41e-2a0e-4e76-a02b-ed36751fb0d0","https://3d.si.edu/object/3d/goniastrea-favulus:7e4dcb32-b69c-4905-aca5-05c0bea7019d","https://3d.si.edu/object/3d/goniastrea-favulus:009463d3-6f58-4f5b-8e60-915805a876ee","https://3d.si.edu/object/3d/goniopora-columna:d85d7078-a2fd-4872-8a81-9d87ba2045cc","https://3d.si.edu/object/3d/heliopora-coerulea:9e0cbb04-1ebc-47df-ae83-7d34486b1de0","https://3d.si.edu/object/3d/heliopora-coerulea:ebea5b5f-5613-4d38-97a2-32e1b8e03ac4","https://3d.si.edu/object/3d/herpetolithus-crassus:980fadc9-3b73-4bc9-892f-dbc4df237354","https://3d.si.edu/object/3d/lactophrys-bicaudalis:b64f9c0a-3634-4043-9b1d-a2aaf2823317","https://3d.si.edu/object/3d/leiopathes-sp:2e7bbd69-c355-473e-a024-d468c05d5a9f","https://3d.si.edu/object/3d/leptoseris-cailleti:09580634-e966-4411-88df-31f37dc9ee0f","https://3d.si.edu/object/3d/leptoseris-cucullata:a2de43d1-df04-4716-bef0-a1397fa1a71f","https://3d.si.edu/object/3d/leptoseris-gardineri:d8e61d2a-b986-4482-9733-fc1d5a6380b9","https://3d.si.edu/object/3d/linckia-laevigata:aff2c3e5-e909-4c18-87ce-8390bac19186","https://3d.si.edu/object/3d/madrepora-aspera:d017d594-05fe-4d3f-963c-e9c6fcdaaa57","https://3d.si.edu/object/3d/madrepora-conigera:1003b2ed-7d72-44c7-9917-9273db332b38","https://3d.si.edu/object/3d/madrepora-cuneata:d8a75768-1e55-4c47-83f3-c41ba3a799c3","https://3d.si.edu/object/3d/madrepora-cytherea:ad22ed7a-d030-4162-8880-e9cd65232514","https://3d.si.edu/object/3d/madrepora-florida:48ab7d3b-c724-4f89-904b-b5b71f57157f","https://3d.si.edu/object/3d/madrepora-formosa:03d6b38a-bf7d-4334-90c9-1f7b4c3041a9","https://3d.si.edu/object/3d/madrepora-horrida:d205464b-97c8-42af-8637-d943137e633d","https://3d.si.edu/object/3d/madrepora-humilis:c921c012-5a3e-4e6f-9c24-7dda761115f4","https://3d.si.edu/object/3d/madrepora-hyacinthus:1a0a3b2d-5ef6-4bc0-af39-0a35d95f1f01","https://3d.si.edu/object/3d/madrepora-robusta:6ec21e42-8a15-49fa-86a0-484485bdf442","https://3d.si.edu/object/3d/madrepora-spicifera:debebbb8-f7ee-4a6d-941c-12ea01dec71a","https://3d.si.edu/object/3d/madrepora-surculosa:fb975479-5faf-4ab7-aaae-6fad92f7fd55","https://3d.si.edu/object/3d/madrepora-tenuis:44f5d73d-2490-45f0-852d-1572c4ab8f01","https://3d.si.edu/object/3d/madrepora-valida:c437bde7-8640-4464-bcad-a01f53a36f75","https://3d.si.edu/object/3d/manopora-caliculata:fd6ccb01-b245-4c9a-9612-ab0224b965a6","https://3d.si.edu/object/3d/manopora-capitata:1385a58a-1ffe-4337-ba19-5540df8ba6ba","https://3d.si.edu/object/3d/manopora-digitata:7ffda3df-e2fc-45ca-8562-fe979f20a3ff","https://3d.si.edu/object/3d/manopora-lichen:0b96ef57-e30b-4e78-a6cb-a2662c32e9f6","https://3d.si.edu/object/3d/manopora-lichen:b7144484-d99d-46a3-9793-73bf0990b8a4","https://3d.si.edu/object/3d/manopora-nodosa:2dffda0b-626f-48be-9ffd-5e042335878b","https://3d.si.edu/object/3d/manopora-scabricula:28d43b47-2706-4bfb-8787-faf2198086a7","https://3d.si.edu/object/3d/meandrina-meandrites:74dc5709-1808-4de3-bce5-bb9be8573d42","https://3d.si.edu/object/3d/merulina-rigida:da58c839-1adb-4840-ae71-7cde6ea78291","https://3d.si.edu/object/3d/merulina-rigida:43b6bd74-b625-4f52-8319-96398697825f","https://3d.si.edu/object/3d/millepora-alcicornis:92c491e7-d31d-403d-b091-316d45dfbc2c","https://3d.si.edu/object/3d/montipora-danae:34b57d25-06d4-42b3-ac95-4c35cb361f6f","https://3d.si.edu/object/3d/odontodactylus-sp:62040f38-ba84-413b-9a24-5b9054e64759","https://3d.si.edu/object/3d/orbicella-curta:aa26e6eb-95b7-4a34-a93a-393231c385ac","https://3d.si.edu/object/3d/panulirus-longipes:baa516b6-ecff-480d-b93e-591dd7ce49c2","https://3d.si.edu/object/3d/pavonia-decussata:694c63cd-aed0-4b01-b4bb-769fc8bec8e7","https://3d.si.edu/object/3d/herpetolithus-crassus:09121e7e-c113-4f2c-a739-cdce13a33cfc","https://3d.si.edu/object/3d/phyllopteryx-taeniolatus:4d6a5e3c-65a0-41e9-81d5-9f4116139471","https://3d.si.edu/object/3d/pocillopora-damicornis:5dbbb9af-2a48-4665-839e-e66faf13ff85","https://3d.si.edu/object/3d/pocillopora-damicornis:14eb9321-2308-4878-8adb-831d078ba0b0","https://3d.si.edu/object/3d/pocillopora-damicornis:ae26ad01-e7be-4664-8a3a-b8bffd42a186","https://3d.si.edu/object/3d/pocillopora-damicornis:3310773f-822e-4376-bd03-2f9d69cfb22c","https://3d.si.edu/object/3d/pocillopora-damicornis:1951c814-3758-4b7f-b0ba-8f996534ff2b","https://3d.si.edu/object/3d/pocillopora-grandis:11012409-827d-4b43-ad7a-1a693645d306","https://3d.si.edu/object/3d/pocillopora-meandrina:16d816f9-4b38-45f5-8add-151182f9a5c4","https://3d.si.edu/object/3d/pocillopora-molokensis:5c844306-0a31-40a2-94f1-8cdc0547dc34","https://3d.si.edu/object/3d/pocillopora-molokensis:7d6d04d4-5758-499f-a69b-e91491fa47a8","https://3d.si.edu/object/3d/porites-lobata:010228bb-75de-4fff-a848-c70584ce1087","https://3d.si.edu/object/3d/porites-monticulosa:32cb1ed0-3d3d-40d7-856f-8d3c599ca0fc","https://3d.si.edu/object/3d/psammocora-columna:1cc58b54-3543-44d7-9fec-6aa89a74c087","https://3d.si.edu/object/3d/pseudodiploria-strigosa:73f73a61-1b87-4dfd-a031-619778b826c0","https://3d.si.edu/object/3d/scolymia-australis:46322c16-a04a-477c-b540-50e9ddf9e9d0","https://3d.si.edu/object/3d/seriatopora-hystrix:4313ff92-0816-476e-aa74-46f296f10074","https://3d.si.edu/object/3d/sideropora-mordax:089a5531-45c5-4306-9842-02966d94db1d","https://3d.si.edu/object/3d/stylaster-alaskanus:83043304-8a8b-4d49-af51-9ddc323b5c91","https://3d.si.edu/object/3d/stylaster-brochi:86591cb1-4b38-4dde-9554-aa9e7d0ba68b","https://3d.si.edu/object/3d/stylaster-sanguineus-valenciennes:6e2f027e-f89b-484b-b6c8-4a8df886ba8b","https://3d.si.edu/object/3d/stylaster-verrillii:d28c1233-8a08-41e5-a23f-6635b043bb69","https://3d.si.edu/object/3d/tridacna-sp:701a39f3-c97a-4951-9de4-1125229eb703","https://3d.si.edu/object/3d/tubipora-musica:6efd0a97-ef3c-4903-a48c-acb6055d5130"]`)
let metadata;

try {
    const rawData = fs.readFileSync('smithsonian_corals/metadata.json', 'utf8'); 
    metadata = JSON.parse(rawData); 
} catch (error) {
    console.log('File does not exist or another error occurred. Using default empty object.');
    metadata = {};
}

const start_index = 0;
const length = 10;
let count = 0;
for(let i = start_index; i < start_index + length; ++i) {
    downloadObj(links[i]).catch(console.error).then(() => {
        console.log('Downloading coral ' + i + ' / ' + length);
        count++;
        if (count === length) {
            fs.writeFileSync('smithsonian_corals/metadata.json', JSON.stringify(metadata, null, 2));
        }
    });
}
