# personnummer [![Build Status](https://secure.travis-ci.org/personnummer/python.png?branch=master)](http://travis-ci.org/personnummer/python)

Validate Swedish social security numbers.

## Installation

```
pip install personnummer
```

or

```
pip3 install personnummer
```

## Example

```python
from personnummer import personnummer

personnummer.valid("0001010107")
# => True
```

See [personnummer/tests/test_personnummer.py](personnummer/tests/test_personnummer.py) for more examples.

## License

MIT