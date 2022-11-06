import { useState, useEffect } from "react";

export default function ServerInfo(props) {

 const [query , setQuery] = useState("pid");
 const [serverstate , setServerState] = useState(
    {
        "running": false,
        "pid": 0,
        "error": false
    }
 );

  function handleClick() {
    fetch(query)
      .then((res) => res.json())
      .then((data) => {
        setResponse(JSON.stringify(data));
      });
  }

  useEffect(() => {
    fetch(`localhost:5000/${query}`)
      .then((res) => res.json())
      .then((data) => {
        setServerState(data);
      });
    }, [serverstate]);
    

  return (
    <div class="QueryButton">
      <button onClick={handleClick}>{description}</button>
      <p>{response}</p>
    </div>
  );

}
