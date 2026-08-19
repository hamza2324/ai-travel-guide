import { useEffect, useState } from "react";
import { NavLink, useLocation } from "react-router-dom";

export function Nav() {
  const { pathname } = useLocation();
  const landing = pathname === "/";
  const [scrolled, setScrolled] = useState(false);

  useEffect(() => {
    if (!landing) {
      setScrolled(false);
      return;
    }
    const onScroll = () => setScrolled(window.scrollY > 48);
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
    return () => window.removeEventListener("scroll", onScroll);
  }, [landing]);

  const classes = ["nav"];
  if (landing) classes.push("nav-over-hero");
  if (landing && scrolled) classes.push("nav-solid");

  return (
    <header className={classes.join(" ")}>
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
