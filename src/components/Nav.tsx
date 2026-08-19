import { NavLink } from "react-router-dom";

export function Nav() {
  return (
    <header className="nav">
      <a className="skip-link" href="#main">
        Skip to content
      </a>
      <NavLink to="/" className="brand">
        <span className="brand-mark" aria-hidden>
          ◈
        </span>
        AI Travel Guide
      </NavLink>
      <nav className="nav-links" aria-label="Primary">
        <NavLink to="/plan">Plan a trip</NavLink>
        <NavLink to="/trips">My trips</NavLink>
        <NavLink to="/plan" className="btn btn-primary btn-small">
          Start planning
        </NavLink>
      </nav>
    </header>
  );
}
