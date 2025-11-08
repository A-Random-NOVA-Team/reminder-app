import React, { useState } from 'react';
import './App.css';
import Reminder from './Reminder';

function App() {

  return (
    <div className="App">

    <div className="row">
    <div className="col-sm-4">placeholder</div>
    <div className="col-sm-8">
      <label>

       <input onKeyDown={(e) => {
                        if (e.key === "Enter") {
                          console.log((e.target as HTMLInputElement).value);
                        }}
                      } />
      </label>
    </div>
    </div>

    </div>
  );
}

export default App;
