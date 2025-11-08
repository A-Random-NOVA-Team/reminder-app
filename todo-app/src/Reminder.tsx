
interface ReminderProps {
  text: string;
  key: string;
  index: number;
  difficultyScore: number;
  completeTaskCallback: (index: number) => void;
}


function Reminder({ text, key, index, difficultyScore, completeTaskCallback }: ReminderProps) {

    return (
        <>
        <div className="row">
            <div className="col-sm-2" onChange={(e) => {
                if ((e.target as HTMLInputElement).checked){
                    completeTaskCallback(index);
                }}}>
                <input type="checkbox"/></div>
            <div className="col-sm-10" style={{ textAlign: 'left' }}>{ text }&nbsp;&nbsp;(+{difficultyScore})</div>
        </div>
        </>
    );
}

export default Reminder;
