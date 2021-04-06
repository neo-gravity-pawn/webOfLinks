# webOfLinks

This is a small crawler for website links within a domain. It creates a graphical output (using [pyvis](https://pyvis.readthedocs.io/en/latest/)) of the link dependencies and their reachability status.

It only has rudimentary functionality (e.g. rough heuristics to identify files, max number of links to parse, an option to ignore query URLs to avoid getting stuck in an calendar or similar fancy page elements ;)).

Feel free to  improve it via pull requests or forks :)

### License

MIT

### Requirements

Python 3.6

### Installation

* Clone this project
* Recommendation: setup a [virtual python environment](https://docs.python.org/3/tutorial/venv.html)
* Install dependencies: `pip install -r requirements.txt`

### Usage

* to crawl provide an URL and and output id: `python3 weboflinks --url https://myurl.com --out myurl`, the resulting files will be located in `/results` and a browser will be opened to show the interactive result visualization (node color legend - red: root, green: internal (ok), orange: internal (broken), purple: external (ok), gray: external (broken), cyan: internal or external file links, white: parsing error)
* to show all parameters `python3 weboflinks -h`
* to run tests: `python3 -m unittest`