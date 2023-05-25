import React from  "react" ;
import Message from "./Message" ;
import History from "./History" ;
import About from "./About" ;

export default function Main() {
    const [navSelection, setNavSelection] = React.useState(0);
    const [main, setMain] = React.useState(<Message />);

    React.useEffect (
        () => {
            if (navSelection === 0) {
                setMain(<Message />);
            } else if (navSelection === 1) {
                setMain(<History />);
            } else if (navSelection === 2) {
                setMain(<About />);
            }
        }, [navSelection]
    )

    return (
        <div className="main">
            <div className="nav">
                <h2>SMS SPAM DETECTOR</h2>
                <ul>
                    <li
                        onClick={() => {
                            setNavSelection(0);
                        }}
                    >
                        MESSAGE
                    </li>
                    <li
                        onClick={() => {
                            setNavSelection(1);
                        }}
                    >
                        HISTORY
                    </li>
                    <li
                        onClick={() => {
                            setNavSelection(2);
                        }}
                    >
                        ABOUT
                    </li>
                </ul>
            </div>
            {main}
        </div>
    );
}