const API_URL = "http://127.0.0.1:8000";

export async function executeCommand(command, shell = "powershell", cwd = null) {
  const response = await fetch(`${API_URL}/api/terminal/execute`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      command,
      shell,
      cwd,
    }),
  });

  if (!response.ok) {
    throw new Error(`Backend error: ${response.status}`);
  }

  return await response.json();
}