const API_URL = "http://127.0.0.1:8000";

export async function getHistory(limit = 100) {
  const response = await fetch(
    `${API_URL}/api/history/?limit=${limit}`
  );

  if (!response.ok) {
    throw new Error("Failed to fetch command history");
  }

  return await response.json();
}

export async function clearHistory() {
  const response = await fetch(
    `${API_URL}/api/history/`,
    {
      method: "DELETE",
    }
  );

  if (!response.ok) {
    throw new Error("Failed to clear command history");
  }

  return await response.json();
}