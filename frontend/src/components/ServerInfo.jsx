import { useEffect, useState } from "react";

export default function ToggleServer(props) {

  const {isRunning} = props
  const [ip, setIp] = useState("")

  useEffect(() => {
    fetch(`/ip`)
      .then((res) => res.json())
      .then((data) => {
        console.log(data.detail);
        setIp(data.detail);
      })
      .catch((err) => {
        setIp("Federated Learning Server Not Running")
      });
  }, [isRunning]);

  return (
    <div className="ToggleServer">
      Server {isRunning ? "Running " : "Not Running "}
      <svg
        width="20"
        height="20"
        viewBox="0 0 20 20"
        fill="none"
        xmlns="http://www.w3.org/2000/svg"
      >
        <circle cx="10" cy="10" r="10" fill={isRunning ? "green" : "red"} />
      </svg>
      <p> {isRunning && `Connect to ${ip}`} </p>
      <hr></hr>
    </div>
     
  );
}
