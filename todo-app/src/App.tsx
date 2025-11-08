import React, { useState } from 'react';
import './App.css';
import Reminder from './Reminder';

function App() {

  const [numReminders, setNumReminders] = useState(3);

  const renderReminders = () => {
    const reminders = [];
    for (let i = 0; i < numReminders; i++) {
      reminders.push(<Reminder key={i}/>);
    }

    return reminders;
  }

  return (
    <div className="App">

    <div className="row">
    <div className="col-sm-4">placeholder</div>
    <div className="col-sm-8">
      <label>

       <input onKeyDown={(e) => {
                        if (e.key === "Enter") {
                          console.log((e.target as HTMLInputElement).value);
                          setNumReminders(prevCount => prevCount + 1);
                        }}
                      } />
      </label>

      {renderReminders()}
    </div>
    </div>

    </div>
  );
}

export default App;
