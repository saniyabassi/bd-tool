# BwB BD Intelligence Tool

A smart business development tool for Bankers without Boundaries. Paste a TOR or RFP and get instant AI-powered analysis.

## What it does

1. **Go / No-Go** — Scores the bid against BwB's competencies and gives a clear recommendation
2. **Relevant Projects** — Surfaces and ranks the best-fit projects from the register with ready-to-use framing
3. **Team Fit** — Matches named TOR roles to BwB team members with fit scores
4. **Draft Text** — Writes a ready-to-paste "Relevant Experience" section and exec summary bullets
5. **Bid Intel** — Effort estimate, competitor landscape, clarifying questions, and risks

---

## Deploy in 15 minutes (free)

### Step 1 — GitHub (2 min)
1. Go to [github.com](https://github.com) and create a free account
2. Click **New repository** → name it `bwb-bd-tool` → Public → Create
3. Upload all files from this folder: `index.html`, `projects.json`, `team.json`

### Step 2 — Netlify (3 min)
1. Go to [netlify.com](https://netlify.com) → Sign up free (use GitHub login)
2. Click **Add new site** → **Import an existing project** → GitHub
3. Select your `bwb-bd-tool` repository
4. Deploy settings: leave everything default → click **Deploy site**
5. Your tool is live at e.g. `bwb-bd-tool.netlify.app`
6. Optional: go to **Domain settings** → rename to `bd.bwb-tool.netlify.app` or similar

### Step 3 — Anthropic API key (2 min)
1. Go to [console.anthropic.com](https://console.anthropic.com)
2. Sign up / log in → **API Keys** → **Create Key**
3. Copy the key (starts with `sk-ant-api03-...`)
4. Each user pastes their own key into the tool on first use
5. Cost: ~$0.01–0.03 per analysis (negligible for BD use)

### Step 4 — Share the link
Send the Netlify URL to the BwB team. That's it.

---

## Updating projects

When you add a new project to the Excel register:

**Option A (quick):** Edit `projects.json` directly on GitHub — add a new entry at the bottom following the same format. Netlify auto-deploys within 60 seconds.

**Option B (auto from Excel):**
```bash
pip install pandas openpyxl
python update_projects.py
```
Then upload the new `projects.json` to GitHub.

---

## Updating team CVs

Edit `team.json` directly on GitHub. For each team member:
- Add their name, title, expertise keywords, sectors, geographies, languages
- Add `highlight_projects` (list of project numbers they've worked on)
- Add `roles_suited` (exact role names as they appear in TORs)

The AI uses these fields to match people to bid roles.

---

## File structure

```
bwb-bd-tool/
├── index.html          ← the whole app (one file)
├── projects.json       ← all 87 projects
├── team.json           ← team CVs
├── update_projects.py  ← script to re-export from Excel
└── README.md           ← this file
```

---

## Notes

- The API key is stored in browser memory only — never logged or stored anywhere
- The tool works on any device with a browser — no installation needed
- All AI calls go directly from the user's browser to Anthropic's API
- Adding the tool to a private GitHub repo + Netlify password protection keeps it internal-only (Netlify free plan supports one password)
