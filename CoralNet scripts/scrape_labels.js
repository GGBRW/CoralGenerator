data = {}
for(let row of document.querySelectorAll('tr:not(:first-child)')) {
    if(row.style.display == 'none') continue;
    const i = row.innerText.split('\t');
    const name = row.querySelectorAll('td')[0].innerText;
    const func = row.querySelectorAll('td')[1].innerText;
    const pop = row.querySelector('.meter').title.slice(0,-1);
    const short = row.querySelectorAll('td')[4].innerText;
    const verif = row.querySelectorAll('td')[3].innerHTML.includes('Verified');
    data[i[0]] = { 'functional group': func, 'default short code': short, 'popularity': pop, 'verified': verif }
}

JSON.stringify(data)