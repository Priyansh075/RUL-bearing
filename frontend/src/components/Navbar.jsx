import { NavLink } from 'react-router-dom'

function Navbar() {
  return (
    <nav className="navbar">
      <div className="navbar-inner">
        <NavLink to="/" className="navbar-brand">
          <span className="brand-icon">⚙️</span>
          <span className="brand-text">Bearing</span>
          <span className="brand-text-accent">AI</span>
        </NavLink>

        <div className="navbar-links">
          <NavLink
            to="/"
            end
            className={({ isActive }) => `nav-link ${isActive ? 'active' : ''}`}
          >
            Dashboard
          </NavLink>
          <NavLink
            to="/predict"
            className={({ isActive }) => `nav-link ${isActive ? 'active' : ''}`}
          >
            Predict RUL
          </NavLink>
          <NavLink
            to="/about"
            className={({ isActive }) => `nav-link ${isActive ? 'active' : ''}`}
          >
            How It Works
          </NavLink>
        </div>
      </div>
    </nav>
  )
}

export default Navbar
