import { Link } from 'react-router-dom'
import { useState, useEffect } from 'react'

function Dashboard() {
  const [modelInfo, setModelInfo] = useState(null)
  const [error, setError] = useState(null)

  useEffect(() => {
    fetch('/api/model-info')
      .then(res => {
        if (!res.ok) throw new Error('Model not loaded')
        return res.json()
      })
      .then(data => setModelInfo(data))
      .catch(() => setError('Model not loaded yet. Please train the model first.'))
  }, [])

  return (
    <div className="page-container">
      {/* Hero */}
      <section className="hero">
        <div className="hero-badge">
          <span className="pulse-dot" />
          Powered by XGBoost & XJTU-SY Data
        </div>

        <h1>
          Predict <span className="gradient-text">Remaining Useful Life</span>
          <br />of Rolling Element Bearings
        </h1>

        <p>
          Upload vibration sensor data and get instant RUL predictions using 
          machine learning. Powered by 28 engineered features extracted from 
          accelerometer signals.
        </p>

        <div className="hero-actions">
          <Link to="/predict" className="btn btn-primary btn-lg">
            🔮 Start Prediction
          </Link>
          <Link to="/about" className="btn btn-secondary btn-lg">
            📖 How It Works
          </Link>
        </div>
      </section>

      {/* Stats */}
      <section className="stats-grid">
        <div className="glass-card stat-card">
          <div className="stat-icon">🎯</div>
          <div className="stat-value cyan">
            {modelInfo ? `${(modelInfo.metrics.test_r2 * 100).toFixed(1)}%` : '—'}
          </div>
          <div className="stat-label">Model R² Accuracy</div>
        </div>
        <div className="glass-card stat-card">
          <div className="stat-icon">📊</div>
          <div className="stat-value emerald">28</div>
          <div className="stat-label">Engineered Features</div>
        </div>
        <div className="glass-card stat-card">
          <div className="stat-icon">⚙️</div>
          <div className="stat-value amber">15</div>
          <div className="stat-label">XJTU-SY Bearings</div>
        </div>
        <div className="glass-card stat-card">
          <div className="stat-icon">⚡</div>
          <div className="stat-value purple">
            {modelInfo ? `${modelInfo.metrics.test_mae.toFixed(1)}` : '—'}
          </div>
          <div className="stat-label">Test MAE (minutes)</div>
        </div>
      </section>

      {/* How it works summary */}
      <section style={{ marginTop: '2rem' }}>
        <div className="section-header" style={{ textAlign: 'center' }}>
          <h2>How It Works</h2>
          <p>From raw vibration signals to RUL prediction in seconds</p>
        </div>

        <div className="pipeline-steps">
          <div className="glass-card pipeline-step">
            <div className="step-number">1</div>
            <h4>Upload Data</h4>
            <p>Upload a CSV file with horizontal & vertical vibration signals from accelerometers</p>
          </div>
          <div className="glass-card pipeline-step">
            <div className="step-number">2</div>
            <h4>Feature Extraction</h4>
            <p>28 time-domain and frequency-domain features are extracted automatically</p>
          </div>
          <div className="glass-card pipeline-step">
            <div className="step-number">3</div>
            <h4>ML Prediction</h4>
            <p>XGBoost model processes the features to predict remaining useful life</p>
          </div>
          <div className="glass-card pipeline-step">
            <div className="step-number">4</div>
            <h4>Health Report</h4>
            <p>View RUL estimate, health status, feature importances, and extracted values</p>
          </div>
        </div>
      </section>

      {/* Model Info */}
      {modelInfo && (
        <section style={{ marginTop: '3rem' }}>
          <div className="section-header" style={{ textAlign: 'center' }}>
            <h2>Model Performance</h2>
            <p>Trained on XJTU-SY bearing degradation data</p>
          </div>

          <div className="stats-grid" style={{ maxWidth: '700px', margin: '1.5rem auto 0' }}>
            <div className="glass-card stat-card">
              <div className="stat-value cyan">{modelInfo.metrics.train_rmse.toFixed(2)}</div>
              <div className="stat-label">Train RMSE (min)</div>
            </div>
            <div className="glass-card stat-card">
              <div className="stat-value amber">{modelInfo.metrics.test_rmse.toFixed(2)}</div>
              <div className="stat-label">Test RMSE (min)</div>
            </div>
            <div className="glass-card stat-card">
              <div className="stat-value emerald">{(modelInfo.metrics.train_r2 * 100).toFixed(1)}%</div>
              <div className="stat-label">Train R²</div>
            </div>
            <div className="glass-card stat-card">
              <div className="stat-value purple">{(modelInfo.metrics.test_r2 * 100).toFixed(1)}%</div>
              <div className="stat-label">Test R²</div>
            </div>
          </div>
        </section>
      )}

      {error && (
        <div className="error-message" style={{ marginTop: '2rem', justifyContent: 'center' }}>
          ⚠️ {error}
        </div>
      )}
    </div>
  )
}

export default Dashboard
