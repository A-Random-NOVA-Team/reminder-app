
interface ReminderProps {
  text: string;
  key: number;
  index: number;
  del: (index: number) => void;
}


function Reminder({ text, key, index, del }: ReminderProps) {

    return (
        <>
        <div className="row">
            <div className="col-sm-2" onClick={() => del(index)}>
                <input type="checkbox"/></div>
            <div className="col-sm-10" style={{ textAlign: 'left' }}>{ text }</div>        
        </div>
        </>
    );
}

export default Reminder;