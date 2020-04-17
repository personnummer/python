# personnummer [![Build Status](https://secure.travis-ci.org/personnummer/python.png?branch=master)](http://travis-ci.org/personnummer/python)

Validate Swedish social security numbers. Version 3+ only supports Python 3.

## Installation

```
pip install personnummer
```

or

```
pip3 install personnummer
```

## Examples

- All examples that uses `personnummer.Personnumer([params])`, can be replaced with `personnummer.parse([params])`.

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
pn = personnummer.Personnummer(8507099805)
pn.format()
# => '850709-9805'

# Long format
pn = personnummer.Personnummer('8507099805')
pn.format(True)
# => '198507099805'
```

### Get Age

```python
from personnummer import personnummer

pn = personnummer.Personnummer("19121212+1212")
pn.get_age()
# => 106
```

See [personnummer/tests/test_personnummer.py](personnummer/tests/test_personnummer.py) for more examples.

## License

MIT
