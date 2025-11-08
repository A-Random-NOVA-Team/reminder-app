function Reminder(props: {text:string, key:number}) {
    
    const handleClick = () => {
        console.log('Button clicked!');
     };

    return (
        <>
        <div className="row">
            <div className="col-sm-2" onClick={handleClick}><input type="checkbox"/></div>
            <div className="col-sm-10" style={{ textAlign: 'left' }}>{ props.text }</div>        
        </div>
        </>
    );
}

export default Reminder;