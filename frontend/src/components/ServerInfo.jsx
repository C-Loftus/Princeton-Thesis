import { Icon } from "@chakra-ui/react";
import { useEffect, useState } from "react";
import ConnectedClients from "./ConnectedClients";

export default function ToggleServer(props) {
  const { isRunning, requiredClients } = props;
  const [ip, setIp] = useState("");

  useEffect(() => {
    fetch(`/api/ip`)
      .then((res) => res.json())
      .then((data) => {
        console.log(data.detail);
        setIp(data.detail);
      })
      .catch((err) => {
        setIp("Federated Learning Server Not Running");
      });
  }, [isRunning]);

  return (
    <div className="ToggleServer">
      Federated Learning Server {isRunning ? "Running " : "Not Running "}
      <Icon viewBox="0 0 200 200">
        <path
          fill={isRunning ? "green" : "red"}
          d="M 100, 100 m -75, 0 a 75,75 0 1,0 150,0 a 75,75 0 1,0 -150,0"
        />
      </Icon>
      <p> {isRunning && `Connect ${requiredClients} Clients to ${ip}`} </p>
      <hr />
      {isRunning && <ConnectedClients />}
      
      <br />
      
    </div>
  );
}
