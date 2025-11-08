
interface ReminderProps {
  text: string;
  key: string;
  index: number;
  del: (index: number) => void;
}


function Reminder({ text, key, index, del }: ReminderProps) {

    return (
        <>
        <div className="row">
            <div className="col-sm-2" onChange={(e) => {
                if ((e.target as HTMLInputElement).checked){
                    del(index);
                }}}>
                <input type="checkbox"/></div>
            <div className="col-sm-10" style={{ textAlign: 'left' }}>{ text }</div>
        </div>
        </>
    );
}

export default Reminder;
