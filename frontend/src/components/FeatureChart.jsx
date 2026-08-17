function FeatureChart({ features, maxBars = 15 }) {
  if (!features || features.length === 0) return null

  const topFeatures = features.slice(0, maxBars)
  const maxImportance = Math.max(...topFeatures.map(f => f.importance))

  const getBarColor = (index) => {
    const colors = [
      'linear-gradient(90deg, #06b6d4, #0891b2)',
      'linear-gradient(90deg, #8b5cf6, #7c3aed)',
      'linear-gradient(90deg, #10b981, #059669)',
      'linear-gradient(90deg, #f59e0b, #d97706)',
      'linear-gradient(90deg, #3b82f6, #2563eb)',
    ]
    return colors[index % colors.length]
  }

  return (
    <div className="feature-chart">
      {topFeatures.map((feat, idx) => {
        const widthPercent = (feat.importance / maxImportance) * 100
        return (
          <div
            key={feat.feature}
            className="feature-bar-row animate-fade-in"
            style={{ animationDelay: `${idx * 50}ms` }}
          >
            <span className="feature-bar-label">{feat.feature}</span>
            <div className="feature-bar-track">
              <div
                className="feature-bar-fill"
                style={{
                  width: `${widthPercent}%`,
                  background: getBarColor(idx),
                }}
              />
            </div>
            <span className="feature-bar-value">
              {(feat.importance * 100).toFixed(1)}%
            </span>
          </div>
        )
      })}
    </div>
  )
}

export default FeatureChart
