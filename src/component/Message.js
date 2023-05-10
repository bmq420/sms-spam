import React from "react" ;
import axios from "axios" ;

export default function Message(props) {
    const [message, setMessage] = React.useState("");
    const [result, setResult] = React.useState("")


    function handleChange(event) {
        setMessage(
            prev => event.target.value
        );
    }

    function clearMessage() {
        setMessage("");
        setResult("")
    }

    function sendMessage() {
        const json = {
            "message": message,
            "available": 1
        }
        console.log(json);
        axios.post("http://localhost:5000/api/v1", json)
            .catch(err => {
                console.log(err);
            })
        async function getResult() {
            const res = await axios.get("http://localhost:5000/api/v1/result")
            console.log(res.data)
            setResult(res.data)
        }
        getResult()
    }

    function displayResult() {
        return (
            <div className="result">
                <p>MODEL'S RESULT</p>
                <p>{result}</p>
            </div>
        )
    }

    return (
        <div className="message">
            <div className="message-box">
                <p>MESSAGE</p>
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