import { useState, useEffect } from "react";

export default function ToggleServer(props) {

  const {isRunning} = props

  return (
    <div class="ToggleServer">
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
      <hr></hr>
    </div>
     
  );
}
