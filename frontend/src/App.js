import { useState } from "react";
import axios from "axios";
import "./App.css";

function App() {
  // new line start
  const [serverData, setServerData] = useState(null);

  function getData(api_url) {
    axios({
      method: "GET",
      url: `/${api_url}`,
    })
      .then((response) => {
        const res = response.data;
        setServerData({
          server_status: res.message,
        });
      })
      .catch((error) => {
        if (error.response) {
          console.log(error.response);
          console.log(error.response.status);
          console.log(error.response.headers);
        }
      });
  }

  return (
    <div className="App">
     
      <header className="App-header">    
      <select
        onChange={(e) => {
          getData(e.target.value);
        }}
      >
        <option value="start">Start Server</option>
        <option value="stop">Stop Server</option>
        <option value="pid">Get PID</option>
      </select>
      {serverData && (
          <div>
            <p>Response from Server: {serverData.server_status}</p>
          </div>
        )}
      </header>
    </div>
  );
}

export default App;
