# CSXhair

[![PyPI release]][pypi] 
[![Python supported versions]][pypi]
[![License]](./LICENSE)

CSXhair is a simple package for decoding/encoding CS:GO (and CS2!) crosshairs using share codes.

```python
from csxhair import Crosshair

my_crosshair = Crosshair.decode('CSGO-ZEw8O-KGXNu-4TTUU-VyXbD-SBCtG')
print(my_crosshair.gap)  # -3.0

my_crosshair.size += 5
my_crosshair.recoil = True  # exclusive to CS2
print(my_crosshair.encode())  # CSGO-hbBNp-7jd43-34SWO-9ck6v-p4FyB

print(my_crosshair.csgo_commands)  # ['cl_crosshairgap -3.0', ..., 'cl_crosshairdot 0', ...]
print(my_crosshair.cs2_commands)  # ['cl_crosshairgap -3.0', ..., 'cl_crosshairdot false', ...]
```

[pypi]: https://pypi.org/project/csxhair/
[PyPI Release]: https://img.shields.io/pypi/v/csxhair.svg?label=pypi&color=green
[Python supported versions]: https://img.shields.io/pypi/pyversions/csxhair.svg?label=%20&logo=python&logoColor=white
[License]: https://img.shields.io/pypi/l/csxhair.svg?style=flat&label=license