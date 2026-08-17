function FeaturesTable({ features }) {
  if (!features) return null

  const entries = Object.entries(features)
  
  // Split into horizontal and vertical features
  const hFeatures = entries.filter(([k]) => k.startsWith('h_'))
  const vFeatures = entries.filter(([k]) => k.startsWith('v_'))

  const formatValue = (val) => {
    if (Math.abs(val) > 10000) return val.toExponential(3)
    if (Math.abs(val) < 0.001) return val.toExponential(3)
    return val.toFixed(4)
  }

  const cleanName = (name) => {
    return name.replace(/^[hv]_/, '').replace(/_/g, ' ')
  }

  return (
    <div style={{ maxHeight: '400px', overflowY: 'auto', borderRadius: 'var(--radius-md)' }}>
      <table className="features-table">
        <thead>
          <tr>
            <th>Feature</th>
            <th>Channel</th>
            <th>Value</th>
          </tr>
        </thead>
        <tbody>
          {hFeatures.map(([key, val]) => (
            <tr key={key}>
              <td>{cleanName(key)}</td>
              <td>
                <span className="feature-channel channel-h">Horizontal</span>
              </td>
              <td>{formatValue(val)}</td>
            </tr>
          ))}
          {vFeatures.map(([key, val]) => (
            <tr key={key}>
              <td>{cleanName(key)}</td>
              <td>
                <span className="feature-channel channel-v">Vertical</span>
              </td>
              <td>{formatValue(val)}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}

export default FeaturesTable
