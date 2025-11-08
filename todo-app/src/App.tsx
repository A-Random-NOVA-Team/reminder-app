import React, { useState } from 'react';
import './App.css';
import Reminder from './Reminder';
import { CreateTaskRequest, Task } from './api/types';
import { getTasks, createTask, updateTask, deleteTask } from './api/tasks';

function App() {

  const [tasks, setTasks] = useState<Task[]>([]);
  const [completedScores, setCompletedScores] = useState(0);

  const fetchTasks = async () => {
    try {
      const tasks = await getTasks();
      setTasks(tasks);
    } catch (error) {
      console.error('Failed to fetch tasks:', error);
    }
  };

  React.useEffect(() => {
    fetchTasks();
  }, []);

  const handleCompleteReminder = (index: number) => {
    const taskScore = tasks[index].diffulty_score || 50;
    updateTask(tasks[index].id, { is_completed: true, difficulty_reestimate: false }).then(() => {
      setCompletedScores(prev => prev + taskScore);
      fetchTasks();
    }).catch(error => {
      console.error('Failed to delete task:', error);
    });
  };

  const renderReminders = () => {
    const reminders = [];

    for (let i = 0; i < tasks.length; i++) {
      reminders.push(
        <Reminder
          key={tasks[i].id}
          text={tasks[i].name}
          index={i}
          del={handleCompleteReminder}
        />
      );
    }

    return reminders;
  }

  const getCharacterEmoji = () => {
    if (completedScores >= 450) return "🤴"; // King
    if (completedScores >= 500) return "⚔️"; // Warrior
    if (completedScores >= 50) return "🛡️"; // Knight
    return "🗡️"; // Squire
  };

  const getCharacterTitle = () => {
    if (completedScores >= 450) return "Legendary Hero";
    if (completedScores >= 500) return "Elite Warrior";
    if (completedScores >= 50) return "Brave Knight";
    return "Noble Squire";
  };

  const getExperiencePercent = () => {
    const nextMilestone = completedScores < 50 ? 50 : completedScores < 450 ? 450 : completedScores < 500 ? 500 : 600;
    const prevMilestone = completedScores < 50 ? 0 : completedScores < 450 ? 50 : completedScores < 500 ? 450 : 500;
    return ((completedScores - prevMilestone) / (nextMilestone - prevMilestone)) * 100;
  };

  return (
    <div className="App">

    <div className="row">

    <div className="col-sm-4">
            <div className="character-panel">
              <div className="character-container">
                <div className="character" style={{
                  transform: completedScores >= 50 ? 'scale(1.1)' : 'scale(1)',
                  filter: completedScores >= 450 ? 'drop-shadow(0 0 20px gold)' : 'drop-shadow(0 5px 15px rgba(0, 0, 0, 0.3))'
                }}>
                  {getCharacterEmoji()}
                </div>
              </div>

              <div className="character-stats">
                <h3>{getCharacterTitle()}</h3>
                <div style={{ fontSize: '14px', color: '#cbd5e0', marginBottom: '10px' }}>
                  Quests Completed: {completedScores}
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
                            const taskName = (e.target as HTMLInputElement).value;
                            if (taskName.trim() === "") return;
                            const newTask: CreateTaskRequest = {
                                name: taskName,
                                description: null,
                                due_date: null,
                            };
                            createTask(newTask).then(() => {
                                (e.target as HTMLInputElement).value = "";
                                fetchTasks();
                            }).catch(error => {
                                console.error('Failed to create task:', error);
                            });
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
