# Lunely

Lunely is a simple Python framework for creating HTTP and WebSocket applications.

## Installation

```bash
git clone https://github.com/your-username/lunely.git
cd lunely
python -m venv .venv
.venv\Scripts\activate
python -m pip install .
```

## Usage

```python
from lunely.http.server import HTTPServer

server = HTTPServer()
server.start()
```

Run the application:

```bash
python examples/basic_app/main.py
```

The server will run at:

```text
http://localhost:8080
```

## Examples

You can find more examples in the `examples/` folder.