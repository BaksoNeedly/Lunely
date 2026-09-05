this framework helps user to create a http and websocket app in an ease.

how to install this project.
1. git clone https://github.com/username/lunely.git
2. cd lunely
3, python -m venv .venv
4. .venv\Scripts\activate
5. python -m pip install .

how to use this project.

you can look at examples/ folder if neccesary.

these are the basic steps to start the server.
1. Create an 'HTTPServer' instance.
server = HTTPServer()

2. Activate the server.
server.start()

3. Run your python file.
python "examples/main.py"