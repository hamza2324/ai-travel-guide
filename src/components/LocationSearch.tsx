import { useEffect, useRef, useState } from "react";
import { api } from "../api";
import type { PlaceSuggestion } from "../types";

interface Props {
  id: string;
  label: string;
  value: string;
  placeholder?: string;
  onChange: (value: string) => void;
  onSelect?: (item: PlaceSuggestion) => void;
}

export function LocationSearch({ id, label, value, placeholder, onChange, onSelect }: Props) {
  const [open, setOpen] = useState(false);
  const [results, setResults] = useState<PlaceSuggestion[]>([]);
  const timer = useRef<number | null>(null);

  useEffect(() => {
    if (value.trim().length < 2) {
      setResults([]);
      return;
    }
    if (timer.current) window.clearTimeout(timer.current);
    timer.current = window.setTimeout(async () => {
      try {
        const data = await api.searchPlaces(value.trim());
        setResults(data.results);
        setOpen(true);
      } catch {
        setResults([]);
      }
    }, 280);
    return () => {
      if (timer.current) window.clearTimeout(timer.current);
    };
  }, [value]);

  return (
    <div className="field search-wrap">
      <label htmlFor={id}>{label}</label>
      <input
        id={id}
        value={value}
        placeholder={placeholder}
        autoComplete="off"
        onChange={(event) => onChange(event.target.value)}
        onFocus={() => results.length && setOpen(true)}
        onBlur={() => window.setTimeout(() => setOpen(false), 180)}
      />
      {open && results.length > 0 && (
        <div className="suggestions" role="listbox" aria-label="Location suggestions">
          {results.map((item) => (
            <button
              key={item.id}
              type="button"
              role="option"
              onMouseDown={(event) => {
                event.preventDefault();
                onChange(item.label);
                onSelect?.(item);
                setOpen(false);
              }}
            >
              <strong>{item.label}</strong>
              {item.subtitle ? <div className="muted">{item.subtitle}</div> : null}
            </button>
          ))}
        </div>
      )}
    </div>
  );
}
