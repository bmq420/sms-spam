import React from "react";
import axios from "axios";

export default function History(props) {
    const [history, setHistory] = React.useState([]);

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

    function clearHistory() {
        axios
            .post("http://localhost:5000/api/v1")
            .then((res) => {
                console.log("Clear history");
            })
            .catch((err) => {
                console.log(err);
            });
    }

    const table = history.map((item, index) => {
        return item.available === 0 ? null : (
            <div className="message-history-element" key={index}>
                {item.message.length > 50 ? (
                    <p className="message-input">
                        {item.message.substring(0, 50) + "..."}{" "}
                    </p>
                ) : (
                    <p className="message-input">{item.message}</p>
                )}
                <p className="message-result bayes">
                    {handleResult(item.bayesResult)}
                </p>
                <p className="message-result backpropagation">
                    {handleResult(item.backpropagationResult)}
                </p>
                <p className="message-result svm">
                    {handleResult(item.svmResult)}
                </p>
                <div className="delete-message" onClick={deleteMessage}>
                    <p onClick={() => deleteMessage(item.id)}>🗑</p>
                </div>
            </div>
        );
    });

    function handleResult(value) {
        if (value === 1) {
            return "SPAM";
        }
        return "HAM";
    }

    function deleteMessage(id) {
        axios
            .post(`http://localhost:5000/api/v1/${id}`)
            .then((res) => {
                console.log("Delete message");
                setHistory((prev) => prev.filter((item) => item.id !== id));
            })
            .catch((err) => {
                console.log(err);
            });
    }

    return (
        <div className="history">
            <h3>MESSAGE HISTORY</h3>
            <div className="history-table-wrap">
                <div className="history-table">
                    <div className="history-table-header">
                        <p style={{ backgroundColor: "#6e6e80" }}>Message</p>
                        <p>Naive - Bayes</p>
                        <p>SVM</p>
                        <p>Backpropagation</p>
                    </div>
                    {table}
                </div>
            </div>
            <div className="history-button">
                <button onClick={clearHistory} className="clear-history">
                    CLEAR HISTORY
                </button>
            </div>
        </div>
    );
}
