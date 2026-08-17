import { useEffect, useState } from 'react'

function RULGauge({ value, maxValue = 125, status = 'healthy' }) {
  const [animatedValue, setAnimatedValue] = useState(0)

  useEffect(() => {
    // Animate from 0 to the target value
    const timer = setTimeout(() => setAnimatedValue(value), 100)
    return () => clearTimeout(timer)
  }, [value])

  const radius = 100
  const circumference = 2 * Math.PI * radius
  const percentage = Math.min(animatedValue / maxValue, 1)
  const dashoffset = circumference * (1 - percentage)

  const getColor = () => {
    switch (status) {
      case 'healthy': return '#10b981'
      case 'warning': return '#f59e0b'
      case 'critical': return '#ef4444'
      default: return '#06b6d4'
    }
  }

  const getStatusLabel = () => {
    switch (status) {
      case 'healthy': return 'Healthy'
      case 'warning': return 'Warning'
      case 'critical': return 'Critical'
      default: return 'Unknown'
    }
  }

  const color = getColor()

  return (
    <div className="rul-gauge-container animate-scale-in">
      <div className="rul-gauge">
        <svg viewBox="0 0 240 240">
          {/* Background circle */}
          <circle
            className="gauge-bg"
            cx="120"
            cy="120"
            r={radius}
          />
          {/* Filled arc */}
          <circle
            className="gauge-fill"
            cx="120"
            cy="120"
            r={radius}
            stroke={color}
            strokeDasharray={circumference}
            strokeDashoffset={dashoffset}
          />
        </svg>
        <div className="gauge-center">
          <div className="gauge-value" style={{ color }}>
            {animatedValue.toFixed(1)}
          </div>
          <div className="gauge-unit">minutes</div>
          <div className="gauge-label">Remaining Life</div>
        </div>
      </div>

      <div className={`health-badge ${status}`}>
        <span className="badge-dot" />
        {getStatusLabel()}
      </div>
    </div>
  )
}

export default RULGauge
