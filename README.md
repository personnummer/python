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

## Examples

### Validation

```python
from personnummer import personnummer

personnummer.valid("0001010107")
# => True

personnummer.valid("19130401+2931")
# => True
```

### Format

```python
from personnummer import personnummer

# Short format
personnummer.format(6403273813)
# => '640327-3813'

# Long format
personnummer.format('6403273813', True)
# => '196403273813'
```

### Get Age
```python
from personnummer import personnummer

personnummer.get_age(6403273813)
# => 55
```

See [personnummer/tests/test_personnummer.py](personnummer/tests/test_personnummer.py) for more examples.

## License

MIT
