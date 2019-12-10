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

personnummer.valid("8507099805")
# => True

personnummer.valid("198507099805")
# => True
```

### Format

```python
from personnummer import personnummer

# Short format
personnummer.format(8507099805)
# => '850709-9805'

# Long format
personnummer.format('8507099805', True)
# => '198507099805'
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
