function About() {
  return (
    <div className="page-container">
      {/* Header */}
      <section className="about-section">
        <div className="hero-badge" style={{ marginBottom: '1.5rem' }}>
          <span className="pulse-dot" />
          Technical Documentation
        </div>
        <h1 style={{ fontSize: 'clamp(1.8rem, 4vw, 2.5rem)', fontWeight: 900, marginBottom: '1rem' }}>
          How <span className="gradient-text">BearingAI</span> Works
        </h1>
        <p style={{ fontSize: '1.1rem', color: 'var(--text-secondary)', maxWidth: '700px' }}>
          An end-to-end machine learning pipeline for predicting the remaining useful life
          of rolling element bearings using vibration signal analysis.
        </p>
      </section>

      {/* Pipeline */}
      <section className="about-section">
        <h2>🔄 Prediction Pipeline</h2>
        <div className="pipeline-steps">
          <div className="glass-card pipeline-step">
            <div className="step-number">1</div>
            <h4>Raw Vibration Data</h4>
            <p>CSV files with 2 channels: horizontal & vertical accelerometer signals sampled at 25.6 kHz</p>
          </div>
          <div className="glass-card pipeline-step">
            <div className="step-number">2</div>
            <h4>Feature Extraction</h4>
            <p>28 statistical features computed: 10 time-domain + 4 frequency-domain per channel</p>
          </div>
          <div className="glass-card pipeline-step">
            <div className="step-number">3</div>
            <h4>Normalization</h4>
            <p>StandardScaler transforms features to zero mean, unit variance for optimal model performance</p>
          </div>
          <div className="glass-card pipeline-step">
            <div className="step-number">4</div>
            <h4>XGBoost Prediction</h4>
            <p>Gradient boosted trees predict RUL in minutes, with feature importance analysis</p>
          </div>
        </div>
      </section>

      {/* Dataset */}
      <section className="about-section">
        <h2>📁 XJTU-SY Dataset</h2>
        <p>
          The XJTU-SY bearing dataset is a widely-used benchmark for bearing prognostics research,
          created by Xi'an Jiaotong University and Changxing Sumyoung Technology Co., Ltd.
        </p>

        <div className="stats-grid" style={{ marginTop: '1.5rem' }}>
          <div className="glass-card stat-card">
            <div className="stat-value cyan">15</div>
            <div className="stat-label">Run-to-Failure Bearings</div>
          </div>
          <div className="glass-card stat-card">
            <div className="stat-value emerald">3</div>
            <div className="stat-label">Operating Conditions</div>
          </div>
          <div className="glass-card stat-card">
            <div className="stat-value amber">25.6 kHz</div>
            <div className="stat-label">Sampling Rate</div>
          </div>
          <div className="glass-card stat-card">
            <div className="stat-value purple">32,768</div>
            <div className="stat-label">Points per Sample</div>
          </div>
        </div>

        <div className="glass-card-static" style={{ marginTop: '1.5rem', overflowX: 'auto' }}>
          <table className="model-comparison-table">
            <thead>
              <tr>
                <th>Operating Condition</th>
                <th>Speed (RPM)</th>
                <th>Radial Load (kN)</th>
                <th>Bearings</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td>Condition 1</td>
                <td>2,100</td>
                <td>12.0</td>
                <td>Bearing 1_1 to 1_5</td>
              </tr>
              <tr>
                <td>Condition 2</td>
                <td>2,250</td>
                <td>11.0</td>
                <td>Bearing 2_1 to 2_5</td>
              </tr>
              <tr>
                <td>Condition 3</td>
                <td>2,400</td>
                <td>10.0</td>
                <td>Bearing 3_1 to 3_5</td>
              </tr>
            </tbody>
          </table>
        </div>
      </section>

      {/* Features */}
      <section className="about-section">
        <h2>📊 Feature Engineering</h2>
        <p style={{ marginBottom: '1.5rem' }}>
          14 features are extracted from each vibration channel (28 total), spanning
          both time-domain and frequency-domain characteristics.
        </p>

        <div className="result-grid">
          <div className="glass-card-static">
            <h3 style={{ marginBottom: '1rem', color: 'var(--accent-cyan)' }}>
              ⏱️ Time-Domain Features (10)
            </h3>
            <div style={{ display: 'grid', gap: '0.5rem' }}>
              {[
                ['RMS', 'Root mean square — overall vibration energy'],
                ['Peak', 'Maximum absolute value — impulse detection'],
                ['Peak-to-Peak', 'Dynamic range of the signal'],
                ['Crest Factor', 'Impulsiveness relative to energy'],
                ['Kurtosis', 'Spikiness — sensitive to early faults'],
                ['Skewness', 'Signal asymmetry indicator'],
                ['Std Deviation', 'Variability of vibration amplitude'],
                ['Shape Factor', 'Waveform shape changes'],
                ['Impulse Factor', 'Impact event detection'],
                ['Margin Factor', 'Sensitive to severe degradation'],
              ].map(([name, desc]) => (
                <div key={name} style={{ padding: '0.5rem 0', borderBottom: '1px solid var(--border-glass)' }}>
                  <div style={{ fontWeight: 600, fontSize: '0.9rem' }}>{name}</div>
                  <div style={{ color: 'var(--text-muted)', fontSize: '0.8rem' }}>{desc}</div>
                </div>
              ))}
            </div>
          </div>

          <div className="glass-card-static">
            <h3 style={{ marginBottom: '1rem', color: 'var(--accent-purple)' }}>
              🌊 Frequency-Domain Features (4)
            </h3>
            <div style={{ display: 'grid', gap: '0.5rem' }}>
              {[
                ['Frequency Center', 'Spectral centroid — mean frequency weighted by power'],
                ['Mean Square Frequency', 'Energy distribution across the frequency spectrum'],
                ['RMS Frequency', 'Square root of mean square frequency'],
                ['Frequency Variance', 'Spread of spectral energy around the centroid'],
              ].map(([name, desc]) => (
                <div key={name} style={{ padding: '0.5rem 0', borderBottom: '1px solid var(--border-glass)' }}>
                  <div style={{ fontWeight: 600, fontSize: '0.9rem' }}>{name}</div>
                  <div style={{ color: 'var(--text-muted)', fontSize: '0.8rem' }}>{desc}</div>
                </div>
              ))}
            </div>

            <h3 style={{ margin: '2rem 0 1rem', color: 'var(--accent-emerald)' }}>
              🏷️ Additional Features (2)
            </h3>
            <div style={{ display: 'grid', gap: '0.5rem' }}>
              {[
                ['Operating Condition', 'Which operating regime (1, 2, or 3) the bearing runs under'],
                ['Normalized Time', 'Position in lifecycle from 0 (start) to 1 (failure)'],
              ].map(([name, desc]) => (
                <div key={name} style={{ padding: '0.5rem 0', borderBottom: '1px solid var(--border-glass)' }}>
                  <div style={{ fontWeight: 600, fontSize: '0.9rem' }}>{name}</div>
                  <div style={{ color: 'var(--text-muted)', fontSize: '0.8rem' }}>{desc}</div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </section>

      {/* Model Selection */}
      <section className="about-section">
        <h2>🤖 Why XGBoost?</h2>
        <p style={{ marginBottom: '1.5rem' }}>
          We evaluated multiple ML approaches. XGBoost was chosen for its superior performance
          on the XJTU-SY dataset's size and structure.
        </p>

        <div className="glass-card-static" style={{ overflowX: 'auto' }}>
          <table className="model-comparison-table">
            <thead>
              <tr>
                <th>Criterion</th>
                <th>XGBoost ✅</th>
                <th>LSTM</th>
                <th>Random Forest</th>
              </tr>
            </thead>
            <tbody>
              <tr className="highlighted">
                <td>Small Dataset (15 bearings)</td>
                <td className="check">✓ Excellent</td>
                <td className="cross">✗ Overfits</td>
                <td>Good</td>
              </tr>
              <tr>
                <td>Training Speed</td>
                <td className="check">✓ Fast (seconds)</td>
                <td className="cross">✗ Slow (hours, GPU)</td>
                <td>Moderate</td>
              </tr>
              <tr className="highlighted">
                <td>Accuracy on Tabular Features</td>
                <td className="check">✓ State-of-the-art</td>
                <td>Good with enough data</td>
                <td>Good</td>
              </tr>
              <tr>
                <td>Interpretability</td>
                <td className="check">✓ Feature importance</td>
                <td className="cross">✗ Black box</td>
                <td className="check">✓ Feature importance</td>
              </tr>
              <tr className="highlighted">
                <td>Deployment</td>
                <td className="check">✓ Simple .joblib file</td>
                <td className="cross">✗ Needs TF/PyTorch</td>
                <td>Simple but larger</td>
              </tr>
              <tr>
                <td>Regularization</td>
                <td className="check">✓ Built-in L1/L2</td>
                <td>Dropout</td>
                <td>Bagging</td>
              </tr>
            </tbody>
          </table>
        </div>
      </section>

      {/* Citation */}
      <section className="about-section">
        <h2>📚 Citation</h2>
        <div className="glass-card-static" style={{ fontFamily: 'var(--font-mono)', fontSize: '0.85rem', color: 'var(--text-secondary)', lineHeight: 1.8 }}>
          Biao Wang, Yaguo Lei, Naipeng Li, Ningbo Li, "A Hybrid Prognostics Approach
          for Estimating Remaining Useful Life of Rolling Element Bearings",
          <em> IEEE Transactions on Reliability</em>, vol. 69, no. 1, pp. 401-412, 2020.
        </div>
      </section>
    </div>
  )
}

export default About
