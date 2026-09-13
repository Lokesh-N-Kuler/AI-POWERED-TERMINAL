import { useEffect, useState } from "react";
import {
  getHistory,
  clearHistory,
} from "../../services/historyService";

function CommandHistory() {
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(true);

  const loadHistory = async () => {
    try {
      const data = await getHistory();
      setHistory(data.history || []);
    } catch (error) {
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  const handleClear = async () => {
    const confirmed = window.confirm(
      "Clear all command history?"
    );

    if (!confirmed) return;

    try {
      await clearHistory();
      setHistory([]);
    } catch (error) {
      console.error(error);
    }
  };

  useEffect(() => {
    loadHistory();
  }, []);

  return (
    <div className="history-container">

      <div className="history-header">
        <div>
          <h2>Command History</h2>
          <p>Previously executed commands</p>
        </div>

        <button onClick={handleClear}>
          Clear History
        </button>
      </div>

      {loading ? (
        <p>Loading history...</p>
      ) : history.length === 0 ? (
        <p>No commands executed yet.</p>
      ) : (
        <div className="history-list">

          {history.map((item) => (
            <div
              className="history-item"
              key={item.id}
            >
              <div className="history-command">
                <span>$</span>
                {item.command}
              </div>

              <div className="history-details">
                <span>
                  Shell: {item.shell}
                </span>

                <span>
                  Exit code: {item.exit_code}
                </span>

                <span>
                  {item.created_at}
                </span>
              </div>

            </div>
          ))}

        </div>
      )}

    </div>
  );
}

export default CommandHistory;