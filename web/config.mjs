export default {
  "title": "Contract Patterns",
  "intro": "Search by vendor or department to see awards, amendment amounts and the original disclosures.",
  "eyebrow": "FEDERAL PROCUREMENT / REPORTED CONTRACTS",
  "accent": "#72513a",
  "tint": "#f2e9df",
  "method": [
    "The rolling collection covers disclosures whose reported contract date lies in the preceding 12 months. This is not a complete amendment census: an amendment may retain an older original contract date.",
    "The source explicitly warns that submissions are unaudited. Disclosure thresholds and procurement rules vary. Amount bands are exploratory controls, not legal tests. Clusters must be checked against source documents before drawing conclusions.",
    "Vendor normalization folds case, punctuation and whitespace; it does not resolve corporate identities or merge similarly named companies by inference. Contract links require both department and a nonempty procurement identifier. Missing or ambiguous links remain explicit.",
    "Award amounts and incremental amendments are kept separate from cumulative reported contract values. Never sum cumulative values as new spending. Reporting quarter is retained because contract date does not necessarily date amendment approval."
  ],
  "id": "contractpatterns",
  "explorer-title": "Search contract disclosures",
  "cadence": "Weekly automated collection. Source dates and capture dates are shown separately.",
  "facets": [
    {
      "key": "department",
      "label": "Department"
    },
    {
      "key": "kind",
      "label": "Record type"
    },
    {
      "key": "year",
      "label": "Contract year"
    }
  ],
  "columns": [
    {
      "key": "vendor",
      "label": "Reported vendor"
    },
    {
      "key": "department",
      "label": "Department"
    },
    {
      "key": "date",
      "label": "Contract date"
    },
    {
      "key": "kind",
      "label": "Record type"
    },
    {
      "key": "amount",
      "label": "Amount (CAD)",
      "money": true
    },
    {
      "key": "contract",
      "label": "Procurement ID"
    }
  ],
  "related": [
    {
      "label": "Cloud Ledger",
      "url": "https://coolcode.ca/cloud-ledger/"
    },
    {
      "label": "Lobby Trail",
      "url": "https://coolcode.ca/lobbytrail/"
    }
  ],
  "controls": [
    {
      "key": "min",
      "label": "Minimum award / amendment (CAD)",
      "type": "number"
    },
    {
      "key": "max",
      "label": "Maximum award / amendment (CAD)",
      "type": "number"
    },
    {
      "key": "days",
      "label": "Award cluster window",
      "options": [
        {
          "value": "7",
          "label": "7 days"
        },
        {
          "value": "30",
          "label": "30 days"
        },
        {
          "value": "90",
          "label": "90 days"
        }
      ],
      "default": "30"
    }
  ]
};
