import React, { useState } from 'react';
import './App.css';
import Reminder from './Reminder';

function App() {

  const [numReminders, setNumReminders] = useState(0);
  const [reminderText, setreminderText] = useState(["test"]);

  const handleDeleteReminder = (index: number) => {
    setreminderText(prevArray => prevArray.filter((_, i) => i !== index));
    setNumReminders(prevCount => prevCount - 1);
  };

  const renderReminders = () => {
    const reminders = [];
    for (let i = 0; i < numReminders; i++) {
      reminders.push(<Reminder text={reminderText[i + 1]} key={i} index={i + 1} del={handleDeleteReminder}/>);
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
                          setreminderText(prevArray => [...prevArray, (e.target as HTMLInputElement).value]);
                          console.log(reminderText);
                          setNumReminders(prevCount => prevCount + 1);
                        }}
                      } />
      </label>

      { renderReminders() }

    </div>
    </div>

    </div>
  );
}

export default App;
