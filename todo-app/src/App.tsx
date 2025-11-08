import React, { useState } from 'react';
import './App.css';
import Reminder from './Reminder';

function App() {

  const [numReminders, setNumReminders] = useState(0);
  const [reminderText, setreminderText] = useState(["test"]);
  const [completedTasks, setCompletedTasks] = useState(0);

  const handleDeleteReminder = (index: number) => {
    setreminderText(prevArray => prevArray.filter((_, i) => i !== index));
    setNumReminders(prevCount => prevCount - 1);
    setCompletedTasks(prev => prev + 1);
  };

  const renderReminders = () => {
    const reminders = [];
    for (let i = 0; i < numReminders; i++) {
      reminders.push(<Reminder text={reminderText[i + 1]} key={i} index={i + 1} del={handleDeleteReminder}/>);
    }

    return reminders;
  }

  const getCharacterEmoji = () => {
    if (completedTasks >= 15) return "🤴"; // King
    if (completedTasks >= 10) return "⚔️"; // Warrior
    if (completedTasks >= 5) return "🛡️"; // Knight
    return "🗡️"; // Squire
  };

  const getCharacterTitle = () => {
    if (completedTasks >= 15) return "Legendary Hero";
    if (completedTasks >= 10) return "Elite Warrior";
    if (completedTasks >= 5) return "Brave Knight";
    return "Noble Squire";
  };

  const getExperiencePercent = () => {
    const nextMilestone = completedTasks < 5 ? 5 : completedTasks < 10 ? 10 : completedTasks < 15 ? 15 : 20;
    const prevMilestone = completedTasks < 5 ? 0 : completedTasks < 10 ? 5 : completedTasks < 15 ? 10 : 15;
    return ((completedTasks - prevMilestone) / (nextMilestone - prevMilestone)) * 100;
  };

  return (
    <div className="App">

    <div className="row">
    
    <div className="col-sm-4">
            <div className="character-panel">
              <div className="character-container">
                <div className="character" style={{
                  transform: completedTasks >= 5 ? 'scale(1.1)' : 'scale(1)',
                  filter: completedTasks >= 10 ? 'drop-shadow(0 0 20px gold)' : 'drop-shadow(0 5px 15px rgba(0, 0, 0, 0.3))'
                }}>
                  {getCharacterEmoji()}
                </div>
              </div>
              
              <div className="character-stats">
                <h3>{getCharacterTitle()}</h3>
                <div style={{ fontSize: '14px', color: '#cbd5e0', marginBottom: '10px' }}>
                  Quests Completed: {completedTasks}
                </div>
                <div style={{ fontSize: '12px', color: '#9ca3af', marginBottom: '5px' }}>
                  Experience
                </div>
                <div className="stat-bar">
                  <div className="stat-fill" style={{ width: `${getExperiencePercent()}%` }}>
                    {Math.round(getExperiencePercent())}%
                  </div>
                </div>
              </div>
            </div>
          </div>

    
    <div className="col-sm-8">

      <div className="quest-header">
              <h1>Quest Board</h1>
              <p>Complete your tasks to level up your hero!</p>
            </div>

      <div className="input-container">
      <label>

       <input type="text" placeholder="Enter a new quest..." onKeyDown={(e) => {
                        if (e.key === "Enter") {
                          setreminderText(prevArray => [...prevArray, (e.target as HTMLInputElement).value]);
                          console.log(reminderText);
                          setNumReminders(prevCount => prevCount + 1);
                        }}
                      } />
      </label>
      </div>

    <div className="quest-list">
      { renderReminders() }
    </div>

    </div>
    </div>

    </div>
  );
}

export default App;
