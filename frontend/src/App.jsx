import Terminal from "./components/Terminal/Terminal";
import CommandHistory from "./components/History/CommandHistory";
import "./index.css";

function App() {
  return (
    <div className="app">

      <header className="app-header">
        <h1>AI-Powered Terminal</h1>
        <p>Intelligent command-line environment</p>
      </header>

      <main className="app-main">

        <Terminal />

        <CommandHistory />

      </main>

    </div>
  );
}

export default App;