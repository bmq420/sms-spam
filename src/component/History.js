import React from "react";
import axios from "axios";

export default function History(props) {
    const [history, setHistory] = React.useState([
    ]);

    React.useEffect(() => {
        axios
            .get("http://localhost:5000/api/v1")
            .then((res) => {
                if (res.data.length !== history.length) {
                    setHistory((prev) => res.data);
                }
            })
            .catch((err) => {
                console.log(err);
            });
    }, [history]);

    console.log(history);

    function clearHistory() {
        axios
            .post("http://localhost:5000/api/v1")
            .then((res) => {
                console.log("Clear history")
            })
            .catch((err) => {
                console.log(err);
            });
    }

    const table = history.map((item, index) => {
        return (
            item.available === 0 ? null : 
            <div className="message-history-element" key={index}>
                {item.message.length > 90 ? 
                    <p className="message-input">{item.message.substring(0, 90) + "..."} </p>
                : 
                    <p className="message-input">{item.message}</p>}
                <p className="message-result">{item.label}</p>
                <div className="delete-message" onClick={deleteMessage}>
                    <p onClick={() => deleteMessage(item.id)}>🗑</p>
                </div>
            </div>
        );
    });

    function deleteMessage(id) {
        axios
            .post(`http://localhost:5000/api/v1/${id}`)
            .then((res) => {
                console.log("Delete message")
                setHistory((prev) => prev.filter((item) => item.id !== id));
            })
            .catch((err) => {
                console.log(err);
            });
    }

    return (
        <div className="history">
            <p>MESSAGE HISTORY</p>
            <div className="history-table-wrap">
                <div className="history-table">{table}</div>
            </div>
            <div className="history-button">
                <button onClick={clearHistory} className="clear-history">
                    CLEAR HISTORY
                </button>
            </div>
        </div>
    );
}
