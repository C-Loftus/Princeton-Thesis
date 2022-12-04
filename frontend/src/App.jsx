import "./App.css";
import ServerInfo from "./components/ServerInfo";
import ServerControl from "./components/ServerControl";
import { useState } from "react";

function App() {
  const [isRunning, setIsRunning] = useState(false);

  return (
    <div className="App">
      <header className="App-header">
        <ServerInfo isRunning={isRunning} />
        <ServerControl setIsRunning={setIsRunning} isRunning={isRunning} />
      </header>
    </div>
  );
}

export default App;
