import React from 'react';
import TablaPersonajes from './TablaPersonajes';
import './App.css';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <h1>Personajes</h1>
        <TablaPersonajes />
        <p>
          Edit <code>src/App.js</code> and save to reload.
        </p>
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React
        </a>
      </header>
    </div>
  );
}

export default App;
