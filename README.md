## AFK Parser

Parse natural-language AFK (away-from-keyboard) phrases into concrete, timezone-aware start and end datetimes.

The core `AFKParser` uses [parsedatetime](https://pypi.org/project/parsedatetime/) under the hood and adds opinionated logic to infer sensible start/end windows for common AFK phrases used in everyday status updates, such as:

- "afk for 30 min"
- "afk till 8am"
- "afk today"
- "afk from 5pm"
- "will start late at 11am"
- "afk on monday"


## Table of contents

- [Features](#features)
- [Installation](#installation)
- [Quick start](#quick-start)
- [Supported phrase patterns](#supported-phrase-patterns-examples)
- [Development](#development)
- [Testing](#testing)
- [Project structure](#project-structure)
- [API reference](#api-reference)
- [Requirements](#requirements)
- [Limitations and notes](#limitations-and-notes)
- [Contributing](#contributing)
- [License](#license)


### Features

- **Natural language parsing** powered by [parsedatetime](https://pypi.org/project/parsedatetime/)
- **Timezone-aware** results; you pass seconds offset from UTC
- **Sensible defaults** for day/week/month/year phrases (e.g., end-of-day windows)
- **Thorough tests** covering many common phrasings


## Installation

### From source

```bash
git clone https://github.com/astr0n0mer/afk_parser.git
cd afk_parser
uv sync --locked
```

This creates a local `.venv` and installs the package with its locked dependencies.

For runtime dependencies only:

```bash
uv sync --locked --no-dev
```

### From PyPI (once published)

```bash
uv add afk-parser
```


## Quick start

### Python API

```python
from datetime import datetime
from afk_parser.afk_parser import AFKParser

# Compute your local UTC offset in seconds (example)
utc_offset_seconds = datetime.now().astimezone().utcoffset().total_seconds()

parser = AFKParser()
result = parser.parse_dates("afk for 30 min", tz_offset=utc_offset_seconds)

if result is not None:
    start_dt, end_dt = result
    print(start_dt, end_dt)
```

`parse_dates` returns a tuple `(start_datetime, end_datetime)` as timezone-aware `datetime` objects, or `None` if the phrase cannot be parsed.

Notes:
- `tz_offset` is a float representing seconds offset from UTC (e.g., `-18000` for UTC-5).
- The parser differentiates between single time points vs. ranges and applies rules like end-of-day for day-level accuracy.

### CLI (from source)

Run the helper script with your phrase. It automatically infers your local UTC offset.

```bash
uv run --locked python main.py "afk from 5pm"
```

Example output (two lines; ISO-8601 repr may vary):

```
2024-06-20 17:00:00-04:00
2024-06-20 23:59:59.999999-04:00
```


## Supported phrase patterns (examples)

These examples are covered by tests and illustrate the behavior. Actual values depend on current date/time and timezone.

- Durations starting now: "afk for 30 min", "afk for 3 hours", "afk for 1 week"
- Until a specific time: "afk till 8am", "afk till 12pm"
- Whole-day windows: "afk today", "afk tomorrow"
- Start at time, end end-of-day: "afk from 5pm", "afk after 5:30pm", "afk post 5pm"
- Specific future times: "will start late at 11am", "will start late at 11am tomorrow"
- Specific days: "afk on monday"
- Month/year ranges: "afk for 1 month", "afk for 2 years" (interpreted as end-of-day windows on the target date)


## Development

Use `uv` to scaffold the environment and install dependencies from `pyproject.toml` and `uv.lock`.

```bash
# Install runtime + dev dependencies
uv sync --locked

# Install runtime dependencies only
uv sync --locked --no-dev
```

Useful commands:

- `uv sync --locked` — create/update `.venv` with locked runtime and dev dependencies
- `uv sync --locked --no-dev` — install locked runtime dependencies only
- `uv run --locked python main.py "afk from 5pm"` — run the source CLI
- `uv run --locked pytest ./afk_parser/tests -vv` — run the test suite
- `uv run --locked pyright .` — run type checks
- `uv run --locked ruff format .` — format the codebase

The `Makefile` wraps the same common tasks if you prefer `make`:

- `make install` — run `uv sync --locked --no-dev`
- `make install_dev` — run `uv sync --locked`
- `make upgrade_dependencies` — upgrade locked dependencies
- `make test` — run the test suite
- `make lint` — run type checks with Pyright
- `make format` — format with Ruff


## Testing

Run the full test suite:

```bash
uv run --locked pytest ./afk_parser/tests -vv
```

Or via the Makefile:

```bash
make test
```


## Project structure

```
afk_parser/
  afk_parser/
    __init__.py
    afk_parser.py      # AFKParser implementation
    tests/
      test_afk_parser.py
  main.py              # Simple CLI wrapper (from source)
  Makefile             # Dev tasks (install, test, lint, format)
  pyproject.toml       # Project metadata and dependencies
  uv.lock              # Locked dependency versions
  setup.py
```


## API reference

```python
class AFKParser:
    def parse_dates(self, phrase: str, tz_offset: float = 0) -> tuple[datetime, datetime] | None
```

- **phrase**: Natural-language AFK phrase
- **tz_offset**: Seconds offset from UTC (float). Use your local offset for local time results.
- Returns a `(start_datetime, end_datetime)` pair as timezone-aware `datetime` objects, or `None` if the phrase could not be parsed.


## Requirements

- Python 3.14+
- `uv`
- `parsedatetime` (installed by `uv sync --locked`)


## Limitations and notes

- Natural language can be ambiguous; not every phrasing is supported. See tests for covered cases.
- Day/month/year phrases are interpreted with end-of-day semantics for the target date.
- For two-part phrases like "from 4pm for 1 hr", the parser computes both start and end precisely to the second.


## Contributing

Issues and PRs are welcome. Before opening a PR, please:

```bash
uv run --locked ruff format .
uv run --locked pyright .
uv run --locked pytest ./afk_parser/tests -vv
```


## License

MIT © Imran Khan. See [LICENSE](./LICENSE) for details.
