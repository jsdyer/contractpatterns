# Contract Patterns

Follow awards, amendments and repeated vendor relationships. Find patterns worth checking against the original disclosures.

Open https://coolcode.ca/contractpatterns/

<!-- coolcode:guide -->
Set a 7-, 30- or 90-day window and an amount band to find repeated awards to the same normalized vendor within a department. Open a row for reported amendments; these patterns are leads, not findings of contract splitting.
<!-- /coolcode:guide -->

## Sources and interpretation

The rolling collection covers disclosures whose reported contract date lies in the preceding 12 months. This is not a complete amendment census: an amendment may retain an older original contract date.

The source explicitly warns that submissions are unaudited. Disclosure thresholds and procurement rules vary. Amount bands are exploratory controls, not legal tests. Clusters must be checked against source documents before drawing conclusions.

Vendor normalization folds case, punctuation and whitespace; it does not resolve corporate identities or merge similarly named companies by inference. Contract links require both department and a nonempty procurement identifier. Missing or ambiguous links remain explicit.

Award amounts and incremental amendments are kept separate from cumulative reported contract values. Never sum cumulative values as new spending. Reporting quarter is retained because contract date does not necessarily date amendment approval.

## Collection and archive

Schedule: **Weekly** (`31 8 * * 3`, UTC). GitHub schedules are best effort. Scheduled and manual runs collect, validate, commit dated snapshots and deploy. A first code push also collects if no saved dataset exists. Other code pushes rebuild the saved dataset offline.

`data/current.json` contains the latest normalized source records and metadata. `archive/YYYY-MM/*.json.gz` retains distinct captured versions; `data/history.json` lists them. Identical data checks update the check time without manufacturing a change. An initial capture is labelled baseline. Archive data is tracked in Git and does not expire with Actions artifacts. The site has snapshot selection, filtering, source detail, CSV export and an RSS change feed.

The default build needs no network. Failed source validation does not replace the published dataset. Optional `HEALTHCHECKS_PING_URL` sends start/success/failure pings for collection runs; no accuracy email is implied.

```sh
python3 -m pip install -r requirements.txt
python3 scripts/collect.py
node --test tests/*.test.mjs
python3 -m unittest discover -s tests -v
python3 scripts/build.py
```

## Privacy

Search and filters are local to the browser; no upstream request is made by filtering. Public data collection runs in GitHub Actions. The shared CoolCode counter records aggregate page opens, without searches or filter values. The explorer and collector run without Cloudflare changes. To enable shared visit counts and private issue reports, add `contractpatterns` to the existing `coolcode-visitor-api` Worker’s `toolList` and deploy it, if not already registered. See the [batch setup notes](https://github.com/jsdyer/jsdyer.github.io/blob/main/docs/tier1-tools.md).

## Software and attribution

Application code is MIT licensed; upstream data retains its original licence and attribution. Follow the source links for original records and terms.

<!-- schedule-reliability -->
## Schedule reliability

Public GitHub repositories can have scheduled workflows disabled after 60 days of inactivity. A separate weekly [schedule guard](.github/workflows/schedule-guard.yml) calls GitHub's enable-workflow API for an explicit list of refresh workflows and itself. It can restore workflows disabled for inactivity, preserves manually disabled workflows, and runs independently of collection failures.

This is an interim mitigation, not a scheduling guarantee: GitHub does not document active-workflow renewal as a permanent exemption, and scheduled runs can be delayed or dropped. A scheduler on our own Linux server is the planned independent trigger. The guard does not collect data, create dummy commits, or change source/check timestamps; successful collection and published data freshness still need monitoring.
<!-- /schedule-reliability -->

## Published freshness

`data/status.json` exposes the existing `checked_at` and `captured_at` from the published dataset without downloading its full records. The watchdog uses `checked_at`: an unchanged successful source check advances it, while an offline build does not.
