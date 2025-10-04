import { useState } from 'react';
import { Cloud, CloudRain, Sun, CloudSnow, Calendar, Clock, MapPin, Zap, Info, Github } from 'lucide-react';

interface ForecastResult {
  time: string;
  prediction: string;
  probabilities: Record<string, number>;
}

const weatherIcons: Record<string, JSX.Element> = {
  'Clear': <Sun className="w-8 h-8 text-yellow-500" />,
  'Rain': <CloudRain className="w-8 h-8 text-blue-500" />,
  'Cloudy': <Cloud className="w-8 h-8 text-gray-500" />,
  'Snow': <CloudSnow className="w-8 h-8 text-blue-300" />,
};

const getWeatherColor = (condition: string): string => {
  const colors: Record<string, string> = {
    'Clear': 'text-yellow-600 bg-yellow-50',
    'Rain': 'text-blue-600 bg-blue-50',
    'Cloudy': 'text-gray-600 bg-gray-50',
    'Snow': 'text-blue-400 bg-blue-50',
  };
  return colors[condition] || 'text-gray-600 bg-gray-50';
};

function App() {
  const [date, setDate] = useState('');
  const [time, setTime] = useState('');
  const [result, setResult] = useState<ForecastResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const checkForecast = async () => {
    if (!date || !time) {
      setError('Please select both date and time');
      return;
    }

    setLoading(true);
    setError('');
    
    try {
      const datetime = `${date}T${time}:00`;
      
      // Call the real LSTM model API
      const response = await fetch('http://localhost:8000/api/v1/forecast', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          city: 'New York City',
          datetime: datetime
        })
      });
      
      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Failed to get forecast');
      }
      
      const result = await response.json();
      setResult(result);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Error fetching forecast. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const getSeasonalContext = () => {
    if (!date) return null;
    
    const month = new Date(date).getMonth();
    const seasons = {
      winter: { months: [11, 0, 1], icon: <CloudSnow className="w-5 h-5" />, desc: "Winter in NYC: Cold with occasional snow and rain" },
      spring: { months: [2, 3, 4], icon: <CloudRain className="w-5 h-5" />, desc: "Spring in NYC: Mild temperatures with frequent rain showers" },
      summer: { months: [5, 6, 7], icon: <Sun className="w-5 h-5" />, desc: "Summer in NYC: Warm and humid with afternoon thunderstorms" },
      fall: { months: [8, 9, 10], icon: <Cloud className="w-5 h-5" />, desc: "Fall in NYC: Cool and crisp with occasional rain" }
    };
    
    for (const [season, data] of Object.entries(seasons)) {
      if (data.months.includes(month)) {
        return { season, ...data };
      }
    }
    return null;
  };

  const seasonalContext = getSeasonalContext();

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50">
      {/* Header */}
      <header className="bg-white/80 backdrop-blur-sm border-b border-gray-200 sticky top-0 z-10">
        <div className="max-w-4xl mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <div className="bg-gradient-to-r from-blue-500 to-purple-600 p-2 rounded-xl">
                <CloudRain className="w-6 h-6 text-white" />
              </div>
              <div>
                <h1 className="text-xl font-bold text-gray-900">Will It Rain On My Parade?</h1>
                <p className="text-sm text-gray-600">NYC Weather Forecasting • Team T-Minus Rain</p>
              </div>
            </div>
            <div className="flex items-center space-x-2 text-sm text-gray-500">
              <Zap className="w-4 h-4" />
              <span>NASA Space Apps 2025</span>
            </div>
          </div>
        </div>
      </header>

      <main className="max-w-4xl mx-auto px-6 py-8">
        {/* Hero Section */}
        <div className="text-center mb-12">
          <div className="inline-flex items-center space-x-2 bg-blue-100 text-blue-800 px-4 py-2 rounded-full text-sm font-medium mb-4">
            <MapPin className="w-4 h-4" />
            <span>New York City Only</span>
          </div>
          <h2 className="text-4xl font-bold text-gray-900 mb-4">
            Plan Your Perfect Parade
          </h2>
          <p className="text-xl text-gray-600 max-w-2xl mx-auto">
            Get AI-powered weather forecasts for your NYC events using our LSTM model trained on NASA open data
          </p>
        </div>

        <div className="grid lg:grid-cols-3 gap-8">
          {/* Input Form */}
          <div className="lg:col-span-2">
            <div className="bg-white rounded-2xl shadow-xl border border-gray-100 p-8">
              <h3 className="text-2xl font-semibold text-gray-900 mb-6 flex items-center">
                <Calendar className="w-6 h-6 mr-3 text-blue-600" />
                When is your event?
              </h3>
              
              <div className="grid md:grid-cols-2 gap-6 mb-8">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Select Date
                  </label>
                  <input
                    type="date"
                    className="w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
                    value={date}
                    onChange={(e) => setDate(e.target.value)}
                    min={new Date().toISOString().split('T')[0]}
                  />
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Select Time
                  </label>
                  <input
                    type="time"
                    className="w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
                    value={time}
                    onChange={(e) => setTime(e.target.value)}
                  />
                </div>
              </div>

              {error && (
                <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-xl text-red-700">
                  {error}
                </div>
              )}

              <button
                onClick={checkForecast}
                disabled={loading || !date || !time}
                className="w-full bg-gradient-to-r from-blue-600 to-purple-600 text-white px-8 py-4 rounded-xl font-semibold text-lg hover:from-blue-700 hover:to-purple-700 disabled:opacity-50 disabled:cursor-not-allowed transition-all transform hover:scale-[1.02] active:scale-[0.98] flex items-center justify-center space-x-2"
              >
                {loading ? (
                  <>
                    <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
                    <span>Analyzing Weather Patterns...</span>
                  </>
                ) : (
                  <>
                    <CloudRain className="w-5 h-5" />
                    <span>Check My Parade Weather</span>
                  </>
                )}
              </button>
            </div>

            {/* Results */}
            {result && (
              <div className="mt-8 bg-white rounded-2xl shadow-xl border border-gray-100 p-8">
                <h3 className="text-2xl font-semibold text-gray-900 mb-6 flex items-center">
                  <Clock className="w-6 h-6 mr-3 text-green-600" />
                  Forecast Results
                </h3>
                
                <div className="bg-gradient-to-r from-gray-50 to-blue-50 rounded-xl p-6 mb-6">
                  <p className="text-lg text-gray-700 mb-4">
                    <strong>Event Time:</strong> {result.time}
                  </p>
                  
                  <div className="flex items-center space-x-4 mb-4">
                    {weatherIcons[result.prediction] || <Cloud className="w-8 h-8 text-gray-500" />}
                    <div>
                      <p className="text-2xl font-bold text-gray-900">{result.prediction}</p>
                      <p className="text-gray-600">Most likely condition</p>
                    </div>
                  </div>
                </div>

                <div>
                  <h4 className="text-lg font-semibold text-gray-900 mb-4">Probability Breakdown</h4>
                  <div className="space-y-3">
                    {Object.entries(result.probabilities)
                      .sort(([,a], [,b]) => b - a)
                      .map(([condition, probability]) => (
                        <div key={condition} className="flex items-center justify-between">
                          <div className="flex items-center space-x-3">
                            {weatherIcons[condition] || <Cloud className="w-5 h-5 text-gray-500" />}
                            <span className="font-medium text-gray-900">{condition}</span>
                          </div>
                          <div className="flex items-center space-x-3">
                            <div className="w-32 bg-gray-200 rounded-full h-2">
                              <div
                                className="bg-gradient-to-r from-blue-500 to-purple-600 h-2 rounded-full transition-all duration-1000"
                                style={{ width: `${probability}%` }}
                              ></div>
                            </div>
                            <span className="text-sm font-semibold text-gray-700 w-12 text-right">
                              {probability}%
                            </span>
                          </div>
                        </div>
                      ))}
                  </div>
                </div>
              </div>
            )}
          </div>

          {/* Sidebar */}
          <div className="space-y-6">
            {/* Seasonal Context */}
            {seasonalContext && (
              <div className="bg-white rounded-2xl shadow-xl border border-gray-100 p-6">
                <h4 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
                  {seasonalContext.icon}
                  <span className="ml-2">Seasonal Context</span>
                </h4>
                <p className="text-gray-600 text-sm leading-relaxed">
                  {seasonalContext.desc}
                </p>
              </div>
            )}

            {/* About */}
            <div className="bg-white rounded-2xl shadow-xl border border-gray-100 p-6">
              <h4 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
                <Info className="w-5 h-5 mr-2 text-blue-600" />
                About This Project
              </h4>
              <div className="space-y-3 text-sm text-gray-600">
                <p>
                  Built for NASA Space Apps 2025 by <strong>Team T-Minus Rain</strong>
                </p>
                <p>
                  Uses an LSTM neural network trained on NASA open weather data to provide accurate forecasts for NYC events.
                </p>
                <div className="pt-3 border-t border-gray-100">
                  <p className="text-xs text-gray-500">
                    <strong>Note:</strong> Forecasts are model predictions and should be used alongside official weather services for critical decisions.
                  </p>
                </div>
              </div>
            </div>

            {/* Features */}
            <div className="bg-white rounded-2xl shadow-xl border border-gray-100 p-6">
              <h4 className="text-lg font-semibold text-gray-900 mb-4">Features</h4>
              <ul className="space-y-2 text-sm text-gray-600">
                <li className="flex items-center">
                  <div className="w-2 h-2 bg-blue-500 rounded-full mr-3"></div>
                  AI-powered LSTM forecasting
                </li>
                <li className="flex items-center">
                  <div className="w-2 h-2 bg-blue-500 rounded-full mr-3"></div>
                  NASA open data integration
                </li>
                <li className="flex items-center">
                  <div className="w-2 h-2 bg-blue-500 rounded-full mr-3"></div>
                  Seasonal weather context
                </li>
                <li className="flex items-center">
                  <div className="w-2 h-2 bg-blue-500 rounded-full mr-3"></div>
                  Probability breakdowns
                </li>
              </ul>
            </div>
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="bg-white border-t border-gray-200 mt-16">
        <div className="max-w-4xl mx-auto px-6 py-8">
          <div className="flex flex-col md:flex-row items-center justify-between">
            <div className="flex items-center space-x-3 mb-4 md:mb-0">
              <div className="bg-gradient-to-r from-blue-500 to-purple-600 p-2 rounded-lg">
                <CloudRain className="w-5 h-5 text-white" />
              </div>
              <div>
                <p className="font-semibold text-gray-900">Team T-Minus Rain</p>
                <p className="text-sm text-gray-600">NASA Space Apps Challenge 2025</p>
              </div>
            </div>
            <div className="flex items-center space-x-4 text-sm text-gray-500">
              <span>NYC Weather Forecasting</span>
              <div className="w-1 h-1 bg-gray-400 rounded-full"></div>
              <span>Powered by LSTM & NASA Data</span>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
}

export default App;