const fs = require('fs');
const path = require('path');

function getFolderNamesSync(folderPath) {
    try {
        // Read directory contents as directory entries
        const entries = fs.readdirSync(folderPath, { withFileTypes: true });
        
        // Filter the entries to get only directories and map to their names
        const folderNames = entries
            .filter(entry => entry.isDirectory())
            .map(dir => dir.name);
        
        return folderNames;
    } catch (error) {
        console.error('Error reading directory:', error);
        return [];
    }
}

const folderPath = 'smithsonian_corals'; // Replace with your target folder path
const folderNames = getFolderNamesSync(folderPath);
// console.log(folderNames);

let zipFileNames = Object.keys(JSON.parse(fs.readFileSync('smithsonian_corals/metadata.json', 'utf8')))
zipFileNames = zipFileNames.map(i => i.replace('.zip', ''))

const glbs = zipFileNames.filter(i => !folderNames.includes(i));



const metadata = JSON.parse(fs.readFileSync('smithsonian_corals/metadata.json', 'utf8'));
console.log(metadata[glbs[0] + '.zip'])


