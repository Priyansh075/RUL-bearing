import { useRef, useState } from 'react'

function FileUpload({ onFileSelect, selectedFile, onClear }) {
  const inputRef = useRef(null)
  const [isDragOver, setIsDragOver] = useState(false)

  const handleDragOver = (e) => {
    e.preventDefault()
    setIsDragOver(true)
  }

  const handleDragLeave = () => {
    setIsDragOver(false)
  }

  const handleDrop = (e) => {
    e.preventDefault()
    setIsDragOver(false)
    const file = e.dataTransfer.files[0]
    if (file && file.name.endsWith('.csv')) {
      onFileSelect(file)
    }
  }

  const handleClick = () => {
    inputRef.current?.click()
  }

  const handleChange = (e) => {
    const file = e.target.files[0]
    if (file) {
      onFileSelect(file)
    }
  }

  const formatSize = (bytes) => {
    if (bytes < 1024) return bytes + ' B'
    if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB'
    return (bytes / (1024 * 1024)).toFixed(1) + ' MB'
  }

  return (
    <div>
      <div
        className={`upload-zone ${isDragOver ? 'drag-over' : ''}`}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
        onClick={handleClick}
      >
        <input
          ref={inputRef}
          type="file"
          accept=".csv"
          onChange={handleChange}
          style={{ display: 'none' }}
        />
        <div className="upload-icon">📊</div>
        <h3>Upload Vibration Data</h3>
        <p>Drag & drop a CSV file with horizontal and vertical vibration signals</p>
        <span className="upload-hint">
          📁 Click to browse or drop CSV file here
        </span>
      </div>

      {selectedFile && (
        <div className="upload-file-info animate-scale-in">
          <span className="file-icon">📄</span>
          <div className="file-details">
            <div className="file-name">{selectedFile.name}</div>
            <div className="file-size">{formatSize(selectedFile.size)}</div>
          </div>
          <button
            className="file-remove"
            onClick={(e) => {
              e.stopPropagation()
              onClear()
            }}
            title="Remove file"
          >
            ✕
          </button>
        </div>
      )}
    </div>
  )
}

export default FileUpload
