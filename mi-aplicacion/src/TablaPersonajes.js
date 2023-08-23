import React, { useState, useEffect } from 'react';
import axios from 'axios';

function TablaPersonajes() {
    const [personajes, setPersonajes] = useState([]);
    const [error, setError] = useState(null);

    useEffect(() => {
        axios.get('http://127.0.0.1:8000/personajes/')
            .then((response) => {
                setPersonajes(response.data);
            })
            .catch((err) => {
                setError(err.message);
            });
    }, []);

    return (
        <div>
            {error ? (
                <div>Error al cargar los personajes: {error}</div>
            ) : (
                <table>
                    <thead>
                        <tr>
                            <th>ID</th>
                            <th>Nombre</th>
                            <th>Edad</th>
                            <th>Origen</th>
                        </tr>
                    </thead>
                    <tbody>
                        {personajes.map((personaje) => (
                            <tr key={personaje.id}>
                                <td>{personaje.id}</td>
                                <td>{personaje.nombre}</td>
                                <td>{personaje.edad}</td>
                                <td>{personaje.origen_id}</td> 
                            </tr>
                        ))}
                    </tbody>
                </table>
            )}
        </div>
    );
}

export default TablaPersonajes;
