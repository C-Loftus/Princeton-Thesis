import { useState, useEffect } from "react";

export default function Test(props) {
  const [ip, setIp] = useState("");

  useEffect(() => {
    fetch(`http://0.0.0.0:8000`)
      .then((res) => res.json())
      .then((data) => {
        console.log(data.detail);
        setIp(data.detail);
      });
  }, []);
  return (
    <div>
      <p> {`Connect Clients to ${ip}`} </p>
      <hr />
      <br />
    </div>
  );
}
