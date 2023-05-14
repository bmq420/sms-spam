import React from "react";
import axios from "axios";

export default function Message(props) {
    const [message, setMessage] = React.useState("");
    const [result, setResult] = React.useState("");
    const [model, setModel] = React.useState(0);

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
            axios.post("http://localhost:5000/api/v1", json).catch((err) => {
                console.log(err);
            });
            async function getResult() {
                const res = await axios.get(
                    "http://localhost:5000/api/v1/result"
                );
                console.log(res.data);
                setResult(res.data);
            }
            getResult();
        }
    }

    function handleModel(event) {
        setModel(event.target.value);
    }

    function displayResult() {
        return (
            <div className="result">
                <h3>MODEL'S RESULT</h3>
                <p>Please select your model: </p>
                <select
                    className="model-result"
                    value={model}
                    onChange={handleModel}
                >
                    <option value="0">-- Choose model</option>
                    <option value="1">Naive - Bayes</option>
                    <option value="2">Support Vector Machine</option>
                    <option value="3">Backpropagation</option>
                </select>
                {model === 1 ? (
                    <p className="bayes-result">{handleResult(result.bayesResult)}</p>
                ) : model === 2 ? (
                    <p className="backpro-result">{handleResult(result.backpropagationResult)}</p>
                ) : model === 3 ? (
                    <p className="svm-result">{handleResult(result.svmResult)}</p>
                ) : (
                    <p></p>
                )}
            </div>
        );
    }

    function handleResult(value) {
        if (value === 1) {
            return "SPAM message";
        }
        return "Not a SPAM message";
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
