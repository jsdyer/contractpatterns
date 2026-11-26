from html import escape
from math import isfinite
import re
from urllib.parse import quote


def money(value):
    return f"CA${value:,.2f}".removesuffix(".00")


def example_card(current, history):
    row = next((r for r in current["records"] if r.get("kind") == "Amendment"
                and isinstance(r.get("amendment_value"), (int, float)) and isfinite(r["amendment_value"])
                and r["amendment_value"] > 0 and all(r.get(k) for k in ("vendor", "department", "reference", "department_id", "reporting_quarter"))), None)
    if not row:
        return '<p>Search the saved disclosures by vendor, department or procurement ID.</p>'
    vendor, department = escape(row["vendor"]), escape(row["department"])
    quarter, reference = escape(row["reporting_quarter"]), escape(row["reference"])
    fiscal = re.fullmatch(r"(\d{4})-(\d{4})-(Q[1-4])", quarter)
    if fiscal:
        first, last, part = fiscal.groups()
        quarter = f"{part} of {first}–{last[-2:]}"
    amount = money(row["amendment_value"])
    url = 'https://search.open.canada.ca/contracts/record/' + quote(row["department_id"], safe="") + ',' + quote(row["reference"], safe="")
    total = row.get("reported_contract_value")
    total_info = f' The cumulative contract value reported in this disclosure was {money(total)}.' if isinstance(total, (int, float)) and isfinite(total) else ''
    return (f'<h2>{vendor}</h2><p>{department} reported an amendment of {amount} for {quarter}.</p>'
            f'<details><summary>Inspect this amendment</summary><p>Disclosure {reference}. '
            f'The {amount} figure is the incremental amendment.{total_info}</p>'
            f'<a href="{escape(url, quote=True)}">Open the federal disclosure</a></details>')
