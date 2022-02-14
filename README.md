Algorithm test
===

### Usage

```bash
$ python3 -m pip install pipenv

# Use virtualenv
$ PIPENV_VENV_IN_PROJECT=true pipenv shell

$ pipenv install --dev
```

- Unittest

```bash
$ pipenv run unittest
```

### References

- [Boyer-Moore string-search algorithm](https://en.wikipedia.org/wiki/Boyer%E2%80%93Moore_string-search_algorithm)

### Solution Notes

- Added Bad Match Table + Good Suffix Table
- View logs while test using:
```bash
$ pipenv run unittest-log
```
- View complete verbose logs while test using:
```bash
$ pipenv run unittest-all-log
```
