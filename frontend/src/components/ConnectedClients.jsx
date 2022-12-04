import { useState, useEffect } from "react";

const POLLING_INTERVAL = 10000;

export default function ConnectedClients(props) {
  const [clients, setClients] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      fetch(`/api/clients`)
        .then((res) => res.json())
        .then((data) => {
          isNaN(data.detail) ? setClients(0) : setClients(data.detail);
        });
    }, POLLING_INTERVAL);

    return () => clearInterval(interval);
  }, []);

  return (
    <div>
      <p> {`${clients} clients connected`} </p>
      <hr />
    </div>
  );
}
