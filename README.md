# personnummer [![Build Status](https://github.com/personnummer/python/workflows/test/badge.svg)](https://github.com/personnummer/python/actions)

Validate Swedish personal identity numbers. Version 3+ only supports Python 3.

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

### Get Date
_New in version 3.2.0_

```python
from personnummer import personnummer

pn = personnummer.Personnummer('19121212+1212')
pn.get_date()
# => datetime.date(1912, 12, 12)
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
