import { useState, useEffect } from "react";

export default function QueryButton(props) {
  const { description, query } = props;
  const [response, setResponse] = useState("");

  function handleClick() {
    fetch(query)
      .then((res) => res.json())
      .then((data) => {
        setResponse(JSON.stringify(data));
      });
  }

  return (
    <div class="QueryButton">
      <button onClick={handleClick}>{description}</button>
      <p>{response}</p>
    </div>
  );

}
