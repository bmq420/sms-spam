import React from "react" ;

export default function Navbar(props) {
    return (
        <div className="nav">
            <h2>SMS SPAM DETECTOR</h2>
            <ul>
                <li>
                    MESSAGE
                </li>
                <li onClick={() => 2}>
                    HISTORY
                </li>
                <li>
                    REPORT
                </li>
                <li>
                    CONTACT
                </li>
            </ul>
        </div>
    );
}