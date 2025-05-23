# cloud-course-project

## Quick start

```bash
pip install cloud-course-project
```

```python
from files_api import ...
```

## Developing/Contributing

### System requirements

You will need the following installed on your machine to develop on this codebase

- `make` AKA `cmake`, e.g. `sudo apt-get update -y; sudo apt-get install cmake -y`
- Python 3.7+, ideally using `pyenv` to easily change between Python versions
- `git`

###

```bash
# clone the repo
git clone https://github.com/<your github username>/cloud-course-project.git

# install the dev dependencies
make install

# run the tests
make test
```

## Following are implemented
- boto3
- testing boto3 (moto)
- testing rest api happy path endpoints
- creating app design pattern using 12-factor app (https://12factor.net/)
- error handling and data validation
- API contracts and docs
  
  