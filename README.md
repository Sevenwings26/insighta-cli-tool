# Insighta CLI

A production-style command line interface for interacting with the Insighta Labs demographic intelligence platform.

The CLI provides authenticated access to:

* Profile intelligence APIs
* Natural language search
* CSV exports
* Secure session management
* Token refresh handling
* Administrative workflows

---

# Features

* GitHub OAuth authentication
* JWT access + refresh token handling
* Automatic token refresh
* API versioning support
* Rich terminal UI
* Structured tables
* CSV export support
* Pagination + filtering
* Natural language querying
* Global installation support

---

# Installation

## 1. Clone the repository

```bash
git clone https://github.com/Sevenwings26/insighta-cli-tool.git
cd insighta-cli-tool
```

---

## 2. Create virtual environment

```bash
python -m venv .venv
```

Activate:

### Windows

```bash
.venv\Scripts\activate
```

### Linux / macOS

```bash
source .venv/bin/activate
```

---

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Install CLI globally

From the project root:

```bash
pip install -e .
```

After installation:

```bash
insighta --help
```

should work from any directory.

---

# Configuration

Credentials are stored automatically at:

```bash
~/.insighta/credentials.json
```

The CLI automatically manages:

* access tokens
* refresh tokens
* token refresh rotation

---

# Authentication

## Login

```bash
insighta login
```

This opens GitHub OAuth authentication in your browser.

After successful authentication:

* access token is stored
* refresh token is stored
* future requests become authenticated automatically

---

## Logout

```bash
insighta logout
```

This revokes the refresh token server-side and clears local credentials.

---

## Current User

```bash
insighta whoami
```

Displays:

* username
* email
* role

---

# Profiles Commands

---

## List Profiles

```bash
insighta profiles list
```

---

## Filter by Gender

```bash
insighta profiles list --gender male
```

---

## Filter by Country

```bash
insighta profiles list --country NG
```

---

## Filter by Age Group

```bash
insighta profiles list --age-group adult
```

---

## Combined Filters

```bash
insighta profiles list \
  --gender male \
  --country NG \
  --age-group adult
```

---

## Age Range

```bash
insighta profiles list \
  --min-age 25 \
  --max-age 40
```

---

## Sorting

```bash
insighta profiles list \
  --sort-by age \
  --order desc
```

Supported sorting fields:

* age
* created_at
* gender_probability

---

## Pagination

```bash
insighta profiles list \
  --page 2 \
  --limit 20
```

---

# Get Single Profile

```bash
insighta profiles get <profile_id>
```

Example:

```bash
insighta profiles get 019dd733-90b2-7573-b486-5b336499697f
```

---

# Create Profile

```bash
insighta profiles create --name "Harriet Tubman"
```

The API automatically enriches the profile using:

* Genderize
* Agify
* Nationalize

---

# Natural Language Search

The CLI supports rule-based natural language querying.

---

## Examples

### Young males from Nigeria

```bash
insighta profiles search "young males from nigeria"
```

---

### Females above 30

```bash
insighta profiles search "females above 30"
```

---

### Adult males from Kenya

```bash
insighta profiles search "adult males from kenya"
```

---

# Export Profiles

Exports filtered datasets as CSV.

---

## Basic Export

```bash
insighta profiles export
```

---

## Filtered Export

```bash
insighta profiles export \
  --gender male \
  --country NG
```

---

## Custom Sorting Export

```bash
insighta profiles export \
  --sort-by age \
  --order desc
```

---

# Export Output

Exports are saved to the current working directory.

Example:

```bash
profiles_export.csv
```

---

# Token Handling

The CLI automatically:

* detects expired access tokens
* refreshes tokens
* retries failed requests

If refresh fails:

```text
Session expired. Please login again.
```

---

# Error Handling

The CLI provides:

* colored terminal errors
* structured API feedback
* authentication warnings
* loading states
* graceful exits

---

# API Requirements

The backend API must support:

* JWT authentication
* refresh token rotation
* API versioning (`X-API-Version: 1`)
* GitHub OAuth
* profile querying endpoints

Default API base URL:

```text
http://127.0.0.1:8000
```

---

# Tech Stack

* Python
* Typer
* Rich
* HTTPX
* FastAPI
* JWT Authentication
* GitHub OAuth
* PostgreSQL

---

# Example Workflow

```bash
# login
insighta login

# view current user
insighta whoami

# list profiles
insighta profiles list --gender female

# search naturally
insighta profiles search "young males from nigeria"

# export dataset
insighta profiles export --country NG

# logout
insighta logout
```

---

# Development Notes

Install editable mode during development:

```bash
pip install -e .
```

This enables live updates to CLI code without reinstalling.

---

# License

MIT License
