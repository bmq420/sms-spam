import React from "react";
import axios from "axios";

export default function Message(props) {
    const [message, setMessage] = React.useState("");
    const [result, setResult] = React.useState("");

    function handleChange(event) {
        setMessage((prev) => event.target.value);
    }

    function clearMessage() {
        setMessage("");
        setResult("");
    }

    function sendMessage() {
        const json = {
            message: message,
            available: 1,
        };
        console.log(json);
        if (message !== "") {
            axios.post("http://localhost:5000/api/v1", json)
            .then((res) => {
                console.log(res.data);
                setResult(res.data);
            })
            .catch((err) => {
                console.log(err);
            });
        }
    }

    function displayResult() {
        return (
            <div className="result">
                <h3>MODEL'S RESULT</h3>
                <div className="result-table-field">
                    {resultTable()}
                </div>
            </div>
        );
    }

    const resultTable = () => {
        return (
            <div className="result-table">
                <div className="result-table-box result-table-bayes">
                    <h4>Naive-Bayes</h4>
                    <p>{handleResult(result.bayesResult)}</p>
                </div>
                <div className="result-table-box  result-table-backpropagation">
                    <h4>Backpropagation</h4>
                    <p>{handleResult(result.backpropagationResult)}</p>
                </div>
                <div className="result-table-box result-table-svm">
                    <h4>SVM</h4>
                    <p>{handleResult(result.svmResult)}</p>
                </div>
            </div>
        );
    }

    function handleResult(result) {
        if (result === 0) {
            return "HAM";
        } else if (result === 1) {
            return "SPAM";
        }
        return "";
    }

    return (
        <div className="message">
            <div className="message-box">
                <h3>MESSAGE</h3>
                <textarea
                    value={message}
                    id=""
                    placeholder="Enter your message here"
                    onChange={handleChange}
                ></textarea>
                <div className="butt">
                    <button onClick={clearMessage}>CLEAR</button>
                    <button onClick={sendMessage}>CHECK</button>
                </div>
                {displayResult()}
            </div>
        </div>
    );
}
