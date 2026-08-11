# Glossary

Everything that came up while building this project, in plain language.
Add your own entries as you go.

---

## The terminal

**Terminal** — a window where you type commands to the operating system directly,
instead of clicking. Not part of any programming language.

**PowerShell** — the terminal that ships with Windows. Its own quirks: `;` instead
of `&&`, commas for multiple folders (`mkdir data, src`).

**Command / argument** — the pattern almost every terminal line follows:
`command argument`. `mkdir quant-lab` = command `mkdir`, argument `quant-lab`.

**Option / flag** — a modifier on a command, written `-m` or `--version`. Some take
a value (`-m "message"`), some are just on/off switches.

**PATH** — the list of folders Windows searches when you type a command name.
If a program isn't on the PATH, you get "not recognized" even though it's installed.

**Execution policy** — a PowerShell setting for whether it will run script files.
`RemoteSigned` = my own scripts run freely, downloaded ones need a signature.

**Script** — a text file containing a list of commands, run top to bottom.
`.ps1` = PowerShell, `.py` = Python, `.sh` = Mac/Linux.

**Interpreted vs compiled** — Python is interpreted: a program reads your text file
line by line and does what it says. C++ is compiled: translated once into a machine
-readable `.exe`. Interpreted = fast to change. Compiled = fast to run.

---

## Environment and packages

**Python interpreter** — `python.exe`, the actual program that runs your code.
Separate from VS Code. Editors and extensions never install languages.

**venv (virtual environment)** — a private copy of Python living inside your project,
with its own libraries. Stops projects with different version needs from breaking
each other.

**activate** — a script that switches your terminal to use the venv's Python instead
of the system one. Lasts only for that terminal window. `(venv)` in the prompt = on.

**Package / library** — a bundle of code someone else wrote that you can use.

**pip** — Python's package installer. It downloads packages; it does not contain them.

**PyPI** — the public server (pypi.org) holding ~600,000 packages that pip downloads from.

**Dependency** — a package required by another package. You install 3, you get 31.

**Install vs import** — `pip install` downloads a package into your venv, once.
`import` loads an already-installed package into the program you're running, every time.

**requirements.txt** — the list of exact package versions your project needs.
Written by `pip freeze > requirements.txt`, recreated by `pip install -r requirements.txt`.

---

## Git

**Git** — version control. Like save points in a game: you periodically record the
state of your files, and can always go back.

**Repository (repo)** — a folder that git is tracking. Created by `git init`, which
makes a hidden `.git` folder holding the history.

**Commit** — one save point, with a message describing what changed.

**Staging** — marking which changes go into the next commit. `git add -A` = all of them.

**.gitignore** — a list of things git should skip. Rule of thumb: if deleting it costs
nothing but a command to regenerate, ignore it. (venv, caches, downloaded data.)

---

## Python basics

**REPL** — the interactive Python prompt (`>>>`). Runs each line as you type it.
Forgets everything when closed. For exploring; files are for keeping.

**Variable** — a name pointing at a value. `data = ...` means "call this thing `data`."

**String** — text, marked by quotes: `"BTC-12AUG26-58000-C"`.

**Function** — a named, reusable block of code. `def fetch(...)` defines one.

**Calling** — running a function, marked by parentheses. `head` refers to it,
`head()` runs it.

**Argument** — a value you hand a function, inside the parentheses.
Positional (`"SPY"`) or named (`start="2015-01-01"`).

**Module** — an imported library, e.g. `requests`. `requests.get()` = a function
inside that module.

**Object** — an actual thing holding data, e.g. a DataFrame.

**Method** — a function attached to an object: `data.to_csv()`. It already knows
what data it's working on, which is why it needs fewer arguments.

**The dot `.`** — "belonging to." `yf.download` = yfinance's download.
`data.to_csv` = this DataFrame's save-as-CSV.

**Indentation** — in Python, the spaces at the start of a line mark what's "inside"
a function or loop. It's syntax, not style.

**f-string** — text with variables dropped in: `f"data/{ticker}.csv"` becomes
`"data/SPY.csv"`.

**Comment** — a line starting with `#` that Python ignores. Notes to humans.

---

## Containers

**List** — an ordered collection. Opened by position: `rows[0]`, `names[:10]`.
Positions start at 0.

**Dictionary (dict)** — a labelled collection of `key: value` pairs. Opened by
name: `d["result"]`.

**The tell** — same square brackets for both. Quotes inside = dict, looking up a
name. Bare number inside = list, looking up a position.

**Index / key** — the position (list) or the name (dict) you use to reach in.

**Nesting** — containers inside containers. API data is usually dicts inside lists
inside dicts. Print one layer at a time when lost.

**Loop (`for`)** — do something once per item. `for i in rows:` — `i` is a temporary
name for whichever item you're holding right now.

**List comprehension** — the compact form of a loop that builds a list:
`[i["strike"] for i in rows]`. The inner brackets open one item; the outer brackets
collect all the results.

**Dict comprehension** — same idea with curly braces, building a dict:
`{i["id"]: i["name"] for i in rows}`.

---

## Investigating data

**`type(x)`** — what kind of thing is this? Tells you which bracket style to use next.

**`len(x)`** — how many items.

**`x.keys()`** — what names are available on a dict. Use this instead of guessing
field names.

**`print(x)`** — show me. Your main tool for seeing inside a running program.

**`pprint(x)`** — pretty print: lays a dict out one field per line.

**`help(f)`** — a function's documentation, printed in the terminal.

**KeyError** — "that name doesn't exist here." Go run `.keys()`.

---

## APIs

**API** — a way for programs to request data from a server, instead of a human
clicking a website.

**Endpoint** — one specific URL that does one specific job, e.g.
`/public/get_instruments`.

**Query parameters** — settings tacked onto a URL after `?`, like
`?currency=BTC&kind=option`. `requests` builds these for you from `params={...}`.

**`requests.get(url, params=...)`** — send a request, get back a Response object.

**JSON** — a text format for structured data. Looks like dicts and lists, but it's
a string until you convert it.

**`r.json()`** — converts that text into real Python dicts and lists.

**JSON-RPC** — the convention Deribit follows: every response is wrapped in an
envelope with `jsonrpc`, plus either `result` (success) or `error` (failure).
This is where `["result"]` comes from.

---

## Options (the finance side)

**Option** — a contract giving the right, but not the obligation, to buy or sell
an asset at a set price by a set date.

**Call / Put** — a call is the right to buy; a put is the right to sell.

**Strike** — the price fixed in the contract.

**Expiry** — the date the contract ends.

**Instrument name** — Deribit's unique ID for one contract:
`BTC-12AUG26-58000-C` = Bitcoin, expiring 12 Aug 2026, $58,000 strike, call.

**Option chain** — all the live options on one underlying, across every strike
and expiry. BTC has ~800 at any moment.

**Underlying** — the asset the option is written on (here, Bitcoin).

**Spot price** — the current price of the underlying itself.

**At the money** — strike close to spot. These trade most, so their prices are
the most trustworthy.

**Implied volatility (IV)** — how much movement the market's price implies it
expects. No formula solves for it directly; it has to be found numerically.
This is the core of the project.

**Adjusted prices** — historical prices corrected for splits and dividends, so
returns reflect what a holder actually experienced.
