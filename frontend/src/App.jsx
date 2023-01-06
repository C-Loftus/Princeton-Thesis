import "./App.css";
import ServerInfo from "./components/ServerInfo";
import ServerControl from "./components/ServerControl";
import { useState } from "react";

function App() {
  const [isRunning, setIsRunning] = useState(false);
  const [requiredClients, setRequiredClients] = useState(0);

  return (
    <div className="App">
      <header className="App-header">
        <ServerInfo isRunning={isRunning} requiredClients={requiredClients}/>
        <ServerControl
          setIsRunning={setIsRunning}
          isRunning={isRunning}
          requiredClients={requiredClients}
          setRequiredClients={setRequiredClients}
        />
      </header>
    </div>
  );
}

export default App;
