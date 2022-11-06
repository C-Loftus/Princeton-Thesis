import { useState } from "react";
import { useEffect } from "react";

export default function ToggleServer(props) {
  const [serverstate, setServerState] = useState(false);
  const [pid , setPid] = useState(0);

  function handleClick() {
    const query = serverstate ? "stop" : "start";
    fetch(query)
      .then((res) => res.json())
      .then((data) => {

        console.log(data.message)
        if (data.message.includes("stopped")) {
            setServerState(false);
        } else if (data.message.includes("started")) {
            setServerState(true);
        }
      })
      .catch((err) => {
        console.log(err);
      });
  }

    useEffect(() => {
        fetch(`/pid`)

        .then((res) => res.json())
        .then((data) => {
            console.log(data.message)
            setPid(data.message);
        })
        .catch((err) => {
            console.log(err);
        });
    }, [serverstate]);


  return (
    <div class="ToggleServer">
      Server {serverstate ? "Running " : "Not Running "}
      <svg
        width="20"
        height="20"
        viewBox="0 0 20 20"
        fill="none"
        xmlns="http://www.w3.org/2000/svg"
      >
        <circle cx="10" cy="10" r="10" fill={serverstate ? "green" : "red"} />
      </svg>
      {pid && <p>Server PID: {pid}</p>}

      <button onClick={handleClick}>
        Turn the server {serverstate ? "off" : "on"}
      </button>
    </div>
  );
}
