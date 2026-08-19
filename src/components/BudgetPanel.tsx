import type { BudgetEstimate } from "../types";

function money(value: number, currency: string) {
  return new Intl.NumberFormat("en-US", {
    style: "currency",
    currency,
    maximumFractionDigits: 0,
  }).format(value);
}

export function BudgetPanel({ budget }: { budget: BudgetEstimate }) {
  const rows = [
    ["Accommodation", budget.accommodation],
    ["Food", budget.food],
    ["Transportation", budget.transportation],
    ["Activities", budget.activities],
    ["Miscellaneous", budget.miscellaneous],
  ] as const;

  return (
    <section className="panel" aria-label="Estimated trip budget">
      <h2 style={{ fontSize: "1.8rem" }}>Estimated trip budget</h2>
      <p className="muted">{budget.disclaimer}</p>
      {rows.map(([label, item]) => (
        <div className="budget-row" key={label}>
          <div>
            <strong style={{ color: "var(--text-primary)" }}>{label}</strong>
            <div className="muted" style={{ fontSize: "0.8rem" }}>
              {item.note}
            </div>
          </div>
          <span>
            {money(item.min, budget.currency)} – {money(item.max, budget.currency)}
          </span>
        </div>
      ))}
      <div className="budget-row" style={{ border: 0, marginTop: 8 }}>
        <strong>Total estimated range</strong>
        <strong>
          {money(budget.total_min, budget.currency)} – {money(budget.total_max, budget.currency)}
        </strong>
      </div>
    </section>
  );
}
