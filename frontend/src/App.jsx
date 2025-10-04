import { useState } from 'react';
import axios from 'axios';

function App() {
  const [date, setDate] = useState('');
  const [time, setTime] = useState('');
  const [result, setResult] = useState(null);

  const checkForecast = async () => {
    try {
      const datetime = `${date}T${time}:00`;
      const res = await axios.post('http://localhost:8000/api/v1/forecast', {
        city: 'New York',
        datetime
      });
      setResult(res.data);
    } catch (err) {
      alert(err.response?.data?.detail || 'Error fetching forecast');
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-100 to-indigo-200 flex flex-col items-center p-6">
      <h1 className="text-3xl font-bold mb-6">Will It Rain On My Parade? 🌦️</h1>
      <p className="mb-4">Team T-Minus Rain — NYC only</p>
      <div className="bg-white rounded-2xl shadow-lg p-6 w-full max-w-md">
        <label className="block mb-2">Select Date</label>
        <input type="date" className="border p-2 rounded w-full mb-4" value={date} onChange={e => setDate(e.target.value)} />
        <label className="block mb-2">Select Time</label>
        <input type="time" className="border p-2 rounded w-full mb-4" value={time} onChange={e => setTime(e.target.value)} />
        <button onClick={checkForecast} className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 w-full">Check My Parade</button>
      </div>

      {result && (
        <div className="mt-6 bg-white rounded-2xl shadow-lg p-6 w-full max-w-md">
          <h2 className="text-xl font-semibold mb-2">Forecast for {result.time}</h2>
          <p className="text-lg">Prediction: <span className="font-bold">{result.prediction}</span></p>
          <h3 className="mt-4 mb-2 font-medium">Probabilities:</h3>
          <ul>
            {Object.entries(result.probabilities).map(([cond, prob]) => (
              <li key={cond}>{cond}: {prob}%</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}

export default App;

