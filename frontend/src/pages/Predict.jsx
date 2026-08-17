import { useState, useEffect } from 'react'
import FileUpload from '../components/FileUpload'
import RULGauge from '../components/RULGauge'
import FeatureChart from '../components/FeatureChart'
import FeaturesTable from '../components/FeaturesTable'

function Predict() {
  const [file, setFile] = useState(null)
  const [operatingCondition, setOperatingCondition] = useState(1)
  const [normalizedTime, setNormalizedTime] = useState(0.5)
  const [result, setResult] = useState(null)
  const [modelInfo, setModelInfo] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  useEffect(() => {
    fetch('/api/model-info')
      .then(res => res.ok ? res.json() : null)
      .then(data => setModelInfo(data))
      .catch(() => {})
  }, [])

  const handlePredict = async () => {
    if (!file) return
    setLoading(true)
    setError(null)
    setResult(null)

    try {
      const formData = new FormData()
      formData.append('file', file)
      formData.append('operating_condition', operatingCondition)
      formData.append('normalized_time', normalizedTime)

      const res = await fetch('/api/predict', {
        method: 'POST',
        body: formData,
      })

      if (!res.ok) {
        const err = await res.json()
        throw new Error(err.detail || 'Prediction failed')
      }

      const data = await res.json()
      setResult(data)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  const handleDemo = async () => {
    setLoading(true)
    setError(null)
    setResult(null)

    try {
      const res = await fetch('/api/predict-demo', { method: 'POST' })
      if (!res.ok) {
        const err = await res.json()
        throw new Error(err.detail || 'Demo prediction failed')
      }
      const data = await res.json()
      setResult(data)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="page-container">
      <div className="section-header">
        <h2>🔮 Predict Remaining Useful Life</h2>
        <p>Upload a vibration CSV file or try a demo prediction</p>
      </div>

      {/* Upload Section */}
      <div className="glass-card-static" style={{ marginBottom: '1.5rem' }}>
        <FileUpload
          onFileSelect={setFile}
          selectedFile={file}
          onClear={() => { setFile(null); setResult(null); }}
        />

        <div className="predict-controls">
          <div className="form-group">
            <label htmlFor="op-condition">Operating Condition</label>
            <select
              id="op-condition"
              value={operatingCondition}
              onChange={(e) => setOperatingCondition(Number(e.target.value))}
            >
              <option value={1}>Condition 1 — 2100 RPM, 12 kN</option>
              <option value={2}>Condition 2 — 2250 RPM, 11 kN</option>
              <option value={3}>Condition 3 — 2400 RPM, 10 kN</option>
            </select>
          </div>

          <div className="form-group">
            <label htmlFor="norm-time">Lifecycle Position (0–1)</label>
            <input
              id="norm-time"
              type="number"
              min="0"
              max="1"
              step="0.05"
              value={normalizedTime}
              onChange={(e) => setNormalizedTime(parseFloat(e.target.value) || 0)}
            />
          </div>

          <div style={{ display: 'flex', gap: '0.5rem' }}>
            <button
              className="btn btn-primary"
              onClick={handlePredict}
              disabled={!file || loading}
            >
              {loading ? '⏳ Analyzing...' : '🔬 Predict'}
            </button>
            <button
              className="btn btn-secondary"
              onClick={handleDemo}
              disabled={loading}
            >
              🎲 Demo
            </button>
          </div>
        </div>
      </div>

      {/* Error */}
      {error && (
        <div className="error-message animate-fade-in">
          ❌ {error}
        </div>
      )}

      {/* Loading */}
      {loading && (
        <div style={{ textAlign: 'center', padding: '3rem' }}>
          <div className="loading-spinner" />
          <p style={{ marginTop: '1rem', color: 'var(--text-secondary)' }}>
            Extracting features & running prediction...
          </p>
        </div>
      )}

      {/* Results */}
      {result && !loading && (
        <div className="animate-fade-in-up">
          {/* Main Result */}
          <div className="glass-card-static" style={{ marginBottom: '1.5rem' }}>
            <div className="result-grid">
              {/* Gauge */}
              <div>
                <RULGauge
                  value={result.predicted_rul}
                  maxValue={125}
                  status={result.health_status}
                />
              </div>

              {/* Signal Info */}
              <div style={{ display: 'flex', flexDirection: 'column', justifyContent: 'center', gap: '1rem' }}>
                <div>
                  <h3 style={{ marginBottom: '1rem', fontSize: '1.2rem' }}>📋 Prediction Summary</h3>
                  
                  <div style={{ display: 'grid', gap: '0.75rem' }}>
                    <div className="glass-card" style={{ padding: '1rem', display: 'flex', justifyContent: 'space-between' }}>
                      <span style={{ color: 'var(--text-secondary)' }}>Predicted RUL</span>
                      <span style={{ fontFamily: 'var(--font-mono)', fontWeight: 700, color: result.health_color }}>
                        {result.predicted_rul} min
                      </span>
                    </div>
                    <div className="glass-card" style={{ padding: '1rem', display: 'flex', justifyContent: 'space-between' }}>
                      <span style={{ color: 'var(--text-secondary)' }}>Health Status</span>
                      <span style={{ fontWeight: 700, color: result.health_color, textTransform: 'capitalize' }}>
                        {result.health_status}
                      </span>
                    </div>
                    <div className="glass-card" style={{ padding: '1rem', display: 'flex', justifyContent: 'space-between' }}>
                      <span style={{ color: 'var(--text-secondary)' }}>Signal Samples</span>
                      <span style={{ fontFamily: 'var(--font-mono)', fontWeight: 600 }}>
                        {result.signal_info.samples.toLocaleString()}
                      </span>
                    </div>
                    <div className="glass-card" style={{ padding: '1rem', display: 'flex', justifyContent: 'space-between' }}>
                      <span style={{ color: 'var(--text-secondary)' }}>Duration</span>
                      <span style={{ fontFamily: 'var(--font-mono)', fontWeight: 600 }}>
                        {result.signal_info.duration_seconds}s
                      </span>
                    </div>
                    <div className="glass-card" style={{ padding: '1rem', display: 'flex', justifyContent: 'space-between' }}>
                      <span style={{ color: 'var(--text-secondary)' }}>Features Used</span>
                      <span style={{ fontFamily: 'var(--font-mono)', fontWeight: 600 }}>
                        {result.features_used}
                      </span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* Feature Importance + Extracted Features */}
          <div className="result-grid">
            {/* Feature Importance */}
            {modelInfo?.feature_importance && (
              <div className="glass-card-static">
                <div className="result-section-title">
                  📊 Feature Importance
                </div>
                <FeatureChart features={modelInfo.feature_importance} maxBars={12} />
              </div>
            )}

            {/* Extracted Features Table */}
            <div className="glass-card-static">
              <div className="result-section-title">
                🔢 Extracted Features
              </div>
              <FeaturesTable features={result.extracted_features} />
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

export default Predict
