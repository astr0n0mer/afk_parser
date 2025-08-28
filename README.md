## AFK Parser

Parse natural-language AFK (away-from-keyboard) phrases into concrete, timezone-aware start and end datetimes.

The core `AFKParser` uses [parsedatetime](https://pypi.org/project/parsedatetime/) under the hood and adds opinionated logic to infer sensible start/end windows for common AFK phrases used in everyday status updates, such as:

- "afk for 30 min"
- "afk till 8am"
- "afk today"
- "afk from 5pm"
- "will start late at 11am"
- "afk on monday"


### Features

- **Natural language parsing** powered by [parsedatetime](https://pypi.org/project/parsedatetime/)
- **Timezone-aware** results; you pass seconds offset from UTC
- **Sensible defaults** for day/week/month/year phrases (e.g., end-of-day windows)
- **Thorough tests** covering many common phrasings


## Installation

### From source (recommended until first PyPI release)

```bash
git clone https://github.com/astr0n0mer/afk_parser.git
cd afk_parser
python -m venv .venv && . .venv/bin/activate
pip install -r requirements.txt
```

For development (linters, tests, tooling):

```bash
make install_dev
```

### From PyPI (once published)

```bash
pip install afk_parser
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
python main.py "afk from 5pm"
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

This repository includes a `Makefile` to simplify common tasks. Use a virtual environment.

```bash
python -m venv .venv
. .venv/bin/activate

# Install runtime deps
make install

# Install dev deps (pytest, ruff, pyright, etc.)
make install_dev
```

Useful commands:

- `make requirements` — regenerate `requirements.txt` and `requirements-dev.txt` from `requirements.in` files
- `make install` — install runtime dependencies
- `make install_dev` — install runtime + dev dependencies
- `make test` — run the test suite
- `make lint` — run type checks with Pyright
- `make format` — format with Ruff


## Testing

Run the full test suite:

```bash
make test
```

Or directly via pytest:

```bash
. .venv/bin/activate
python -m pytest ./afk_parser/tests -vv
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
  requirements*.txt
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

- Python 3.10+
- `parsedatetime` (installed via requirements)


## Limitations and notes

- Natural language can be ambiguous; not every phrasing is supported. See tests for covered cases.
- Day/month/year phrases are interpreted with end-of-day semantics for the target date.
- For two-part phrases like "from 4pm for 1 hr", the parser computes both start and end precisely to the second.


## Contributing

Issues and PRs are welcome. Before opening a PR, please:

```bash
make format
make lint
make test
```


## License

MIT © Imran Khan. See [LICENSE](./LICENSE) for details.


