import "./App.css";
import ToggleServer from "./components/ToggleServer";
import ServerForm from "./components/ServerForm";

function App() {

  return (
    <div className="App">
      <header className="App-header">
      <ToggleServer />
      <ServerForm/>

      </header>
    </div>
  );
}

export default App;
