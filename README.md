# CSXhair

[![PyPI release]][pypi] 
[![Python supported versions]][pypi]
[![License]](./LICENSE)

CSXhair is a simple package for decoding, changing and encoding CS2 crosshairs using game share codes.

> [!WARNING]
> Since CS2's [Rush Hour update](https://www.counter-strike.net/newsentry/711161056325533826) 
> CS:GO and early CS2 crosshair share codes are no longer supported.
> 
> For CS:GO crosshair support, use [version 1.0.1](https://pypi.org/project/csxhair/1.0.1/) of the package.

```python
from csxhair import Crosshair

my_crosshair = Crosshair.decode('CSjNcfcGjo8LLy2pDpCynr5e5efCGW6yXuf7B6aQ7wkWmU')
print(my_crosshair.gap)  # 2

my_crosshair.length += 5
my_crosshair.recoil = True
print(my_crosshair.encode())  # CSpQo2QSOSE2jXKTFHKei7T4mK5fznKeT2ziT8qXK9uN3Z

print(my_crosshair.commands) # ['cl_crosshair_drawoutline 0', ..., 'cl_ironsight_usecrosshaircolor true', 'cl_ironsight_dot_scale 1.0']
```

*Special thanks to [Aquarius](https://github.com/aquaismissing) for making a rough implementation led to this package.*

[pypi]: https://pypi.org/project/csxhair/
[PyPI Release]: https://img.shields.io/pypi/v/csxhair.svg?label=pypi&color=green
[Python supported versions]: https://img.shields.io/pypi/pyversions/csxhair.svg?label=%20&logo=python&logoColor=white
[License]: https://img.shields.io/pypi/l/csxhair.svg?style=flat&label=license