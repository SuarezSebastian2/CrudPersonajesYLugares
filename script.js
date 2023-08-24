function loadCharacters() {
    fetch('http://127.0.0.1:5000/characters')
        .then(response => response.json())
        .then(characters => {
            const table = document.getElementById('characters-table');
            table.innerHTML = '';
            characters.forEach(character => {
                const row = table.insertRow();
                row.insertCell(0).innerHTML = character.id;
                row.insertCell(1).innerHTML = character.nombre;
                row.insertCell(2).innerHTML = character.edad;
                row.insertCell(3).innerHTML = character.origen_id;
                const actions = row.insertCell(4);
                const deleteButton = document.createElement('button');
                deleteButton.className = 'btn btn-danger';
                deleteButton.innerText = 'Delete';
                deleteButton.onclick = () => deleteCharacter(character.id);
                actions.appendChild(deleteButton);
            }); // Esta es la llave de cierre correcta para el forEach
        })
        .catch(error => console.error('Error:', error));
}


function loadLocations() {
    fetch('http://127.0.0.1:5000/locations')
        .then(response => response.json())
        .then(locations => {
            const table = document.getElementById('locations-table');
            table.innerHTML = '';
            locations.forEach(location => {
                const row = table.insertRow();
                row.insertCell(0).innerHTML = location.id;
                row.insertCell(1).innerHTML = location.nombre;
                row.insertCell(2).innerHTML = location.descripcion;
                const actions = row.insertCell(3);
                const deleteButton = document.createElement('button');
                deleteButton.className = 'btn btn-danger';
                deleteButton.innerText = 'Delete';
                deleteButton.onclick = () => deleteLocation(location.id);
                actions.appendChild(deleteButton);
            });
        });
}

function addCharacter(event) {
    event.preventDefault();
    const name = document.getElementById('character-name').value;
    const age = document.getElementById('character-age').value;
    const originId = document.getElementById('character-origin-id').value;
    fetch('http://127.0.0.1:5000/character', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ nombre: name, edad: age, origen_id: originId })
    }).then(() => loadCharacters());
}

function addLocation(event) {
    event.preventDefault();
    const name = document.getElementById('location-name').value;
    const description = document.getElementById('location-description').value;
    fetch('http://127.0.0.1:5000/location', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ nombre: name, descripcion: description })
    }).then(() => loadLocations());
}

function deleteCharacter(id) {
    fetch(`http://127.0.0.1:5000/character/${id}`, { method: 'DELETE' }).then(() => loadCharacters());
}

function deleteLocation(id) {
    fetch(`http://127.0.0.1:5000/location/${id}`, { method: 'DELETE' }).then(() => loadLocations());
}

document.getElementById('character-form').addEventListener('submit', addCharacter);
document.getElementById('location-form').addEventListener('submit', addLocation);
