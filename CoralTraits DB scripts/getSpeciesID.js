// Function to get the numbers for the given species names
function getSpeciesNumbers(speciesArray) {
    // Get all the list items
    let speciesNumbers = {};
  
    listItems.forEach(item => {
      let number = item.querySelector('.col-sm-1').textContent.trim();
      let speciesName = item.querySelector('.col-sm-5 a').textContent.trim();
      
      if (speciesArray.includes(speciesName)) {
        speciesNumbers[speciesName] = number;
      }
    });
  
    return speciesNumbers;
  }

  let listItems = document.querySelectorAll('.list-group li');
  listItems = Array.from(listItems).slice(1)
  
  // Call the function and log the result
  let result = getSpeciesNumbers(speciesArray);
  console.log(result);