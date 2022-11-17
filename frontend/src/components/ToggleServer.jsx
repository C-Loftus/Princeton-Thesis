import { useState, useEffect } from "react";

export default function ToggleServer(props) {
  const [serverstate, setServerState] = useState(false);
  const [pid, setPid] = useState(0);

  function handleClick() {
    const query = serverstate ? "stop" : "start";
    fetch(query)
      .then((res) => {
        if (res.ok) {
          setServerState(!serverstate);
        }
        res.json();
      })
      .then((data) => {
        console.log(data.message);
      })
      .catch((err) => {
        console.log(err);
      });
  }

  useEffect(() => {
    fetch(`/pid`)
      .then((res) => res.json())
      .then((data) => {
        console.log(data.message);
        setPid(data.detail);
      })
      .catch((err) => {
        console.log(err);
      });

    fetch(`/running`)
      .then((res) => res.json())
      .then((data) => {
        console.log(data.detail);
        setServerState(data.detail);
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
      <hr></hr>
      <button onClick={handleClick}>
        Turn the server {serverstate ? "off" : "on"}
      </button>
    </div>
     
  );
}
