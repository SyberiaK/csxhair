from __future__ import annotations

from re import compile as re_compile
from sys import version_info

from attrs import Attribute, define, field


__version__ = '2.0.0'
__all__ = ('Crosshair',)
__author__ = 'SyberiaK <syberiakey@gmail.com>'

DICTIONARY = 'ABCDEFGHJKLMNOPQRSTUVWXYZabcdefhijkmnopqrstuvwxyz23456789'
DICTIONARY_LENGTH = len(DICTIONARY)
CODE_PATTERN = re_compile(r'CSGO(-[{%s}]{5}){5}$' % DICTIONARY)


if version_info >= (3, 15):
    # noinspection PyUnresolvedReferences
    to_bytes = bytearray.take_bytes  # doesn't do a copy
else:
    to_bytes = bytes


def signed_byte(x: int, /) -> int:
    """Converts an unsigned byte to a signed one."""

    return (x ^ 0x80) - 0x80  # https://stackoverflow.com/a/37095855


def lowercase_bool(x: bool, /) -> str:
    """For the sake of values unifying - returns a lowercase string of bool (``'True'`` -> ``'true'``)."""

    if type(x) is bool:
        return str(x).lower()

    raise ValueError(f'Expected bool, got {x}')


def _validate_bounds(lower_bound: int | float, upper_bound: int | float, /):
    def inner(_, attribute: Attribute, value: int):
        if not (lower_bound <= value <= upper_bound):
            raise ValueError(f"'{attribute.name}' has to be in range [{lower_bound}; {upper_bound}].")

    return inner


@define
class Crosshair:
    """Represents a CS:GO/CS2 crosshair."""

    gap: float = field(validator=_validate_bounds(-12.8, 12.7))
    """
    Command: ``cl_crosshair_gap``

    [-12.8; 12.7]
    """

    red: int = field(validator=_validate_bounds(0, 255))
    """
    Command: ``cl_crosshaircolor_r``

    [0; 255]
    """

    green: int = field(validator=_validate_bounds(0, 255))
    """
    Command: ``cl_crosshaircolor_g``

    [0; 255]
    """

    blue: int = field(validator=_validate_bounds(0, 255))
    """
    Command: ``cl_crosshaircolor_b``

    [0; 255]
    """

    alpha: int = field(validator=_validate_bounds(0, 255))
    """
    Command: ``cl_crosshaircolor_a``

    [0; 255]
    """

    dynamic_splitdist: int = field(validator=_validate_bounds(0, 127))
    """
    Command: ``cl_crosshair_dynamic_splitdist``

    [0; 127]
    """

    dynamic_spread_limit: int = field(validator=_validate_bounds(0, 255))
    """
    Command: ``cl_crosshair_dynamic_spread_limit``

    [0; 255]
    """

    recoil: bool = field(converter=bool)
    """
    Command: ``cl_crosshair_recoil``
    """

    draw_outline: int = field(validator=_validate_bounds(0, 2))
    """
    Command: ``cl_crosshair_drawoutline``

    [0; 2]
    """

    dynamic_splitalpha_innermod: float = field(validator=_validate_bounds(0, 1))
    """
    Command: ``cl_crosshair_dynamic_splitalpha_innermod``

    [0.0; 1.0]
    """

    dynamic_splitalpha_outermod: float = field(validator=_validate_bounds(0.3, 1))
    """
    Command: ``cl_crosshair_dynamic_splitalpha_outermod``

    [0.3; 1.0]
    """

    dynamic_maxdist_split_ratio: float = field(validator=_validate_bounds(0, 1))
    """
    Command: ``cl_crosshair_dynamic_maxdist_splitratio``

    [0.0; 1.0]
    """

    thickness: int = field(validator=_validate_bounds(0, 6.3))
    """
    Command: ``cl_crosshair_thickness``

    [0; 32]
    """

    style: int = field(validator=_validate_bounds(0, 5))
    """
    Command: ``cl_crosshairstyle``

    [0; 5]
    """

    dot: bool = field(converter=bool)
    """
    Command: ``cl_crosshairdot``
    """

    t: bool = field(converter=bool)
    """
    Command: ``cl_crosshair_t``
    """

    length: int = field(validator=_validate_bounds(0, 255))
    """
    Command: ``cl_crosshair_length``

    [0; 255]
    """

    _screen_height: int = 1080
    """
    Stored in the crosshair code for compatibility sake.
    
    In most cases, it really just produces different sharecodes for the same crosshair.
    """

    @property
    def cs2_commands(self) -> list[str]:
        """List of commands to apply this crosshair in CS2."""

        return [
            f'cl_crosshair_gap {self.gap}',
            f'cl_crosshaircolor_r {self.red}',
            f'cl_crosshaircolor_g {self.green}',
            f'cl_crosshaircolor_b {self.blue}',
            f'cl_crosshaircolor_a {self.alpha}',
            f'cl_crosshair_dynamic_splitdist {self.dynamic_splitdist}',
            f'cl_crosshair_dynamic_spread_limit {self.dynamic_spread_limit}',
            f'cl_crosshair_recoil {lowercase_bool(self.recoil)}',
            f'cl_crosshair_drawoutline {self.draw_outline}',
            f'cl_crosshair_dynamic_splitalpha_innermod {self.dynamic_splitalpha_innermod}',
            f'cl_crosshair_dynamic_splitalpha_outermod {self.dynamic_splitalpha_outermod}',
            f'cl_crosshair_dynamic_maxdist_splitratio {self.dynamic_maxdist_split_ratio}',
            f'cl_crosshairthickness {self.thickness}',
            f'cl_crosshairstyle {self.style}',
            f'cl_crosshairdot {lowercase_bool(self.dot)}',
            f'cl_crosshair_t {lowercase_bool(self.t)}',
            f'cl_crosshair_length {self.length}'
        ]

    @staticmethod
    def decode_to_bytes(code: str) -> bytes:

        if not CODE_PATTERN.match(code):
            raise ValueError(f"{code!r} doesn't match the pattern.")

        chars = code[5:].replace('-', '')

        num = 0
        for c in reversed(chars):
            num = num * DICTIONARY_LENGTH + DICTIONARY.index(c)

        hexnum = hex(num)[2:].zfill(36)
        try:
            _bytes = bytes.fromhex(hexnum)
        except ValueError:
            raise ValueError(f'Invalid crosshair code: {code!r}.')

        if _bytes[0] != sum(_bytes[1:]) % 256:
            raise ValueError(f'Invalid crosshair code: {code!r}.')

        return _bytes

    @staticmethod
    def decode(code: str) -> Crosshair:
        """
        Translates a crosshair share code into a Crosshair object.

        Parameters:
            code (str):
                a crosshair share code.

        Returns:
            a Crosshair object assosiated with this code.

        Raises:
            ValueError: if the code is invalid.
        """

        if not CODE_PATTERN.match(code):
            raise ValueError(f"{code!r} doesn't match the pattern.")

        chars = code[5:].replace('-', '')

        num = 0
        for c in reversed(chars):
            num = num * DICTIONARY_LENGTH + DICTIONARY.index(c)

        hexnum = hex(num)[2:].zfill(36)
        try:
            _bytes = bytes.fromhex(hexnum)
        except ValueError:
            raise ValueError(f'Invalid crosshair code: {code!r}.')

        if _bytes[0] != sum(_bytes[1:]) % 256:
            raise ValueError(f'Invalid crosshair code: {code!r}.')

        sorted_bytes = Crosshair._sort_bytes(_bytes)

        return Crosshair(**sorted_bytes)

    @staticmethod
    def _sort_bytes(_bytes):
        return {
            'style': _bytes[2] & 7,
            'recoil': (_bytes[2] & 16) != 0,
            'dot': (_bytes[2] & 64) != 0,
            't': (_bytes[2] & 128) != 0,
            'red': _bytes[3],
            'green': _bytes[4],
            'blue': _bytes[5],
            'alpha': _bytes[6],
            'gap': _bytes[7],
            'length': _bytes[8],
            'dynamic_spread_limit': _bytes[9],
            'dynamic_splitdist': _bytes[10] & 127,
            'dynamic_splitalpha_innermod': (_bytes[11] & 127) / 10,
            'dynamic_splitalpha_outermod': 0.3 + (_bytes[11] >> 7) / 20,
            'dynamic_maxdist_split_ratio': (_bytes[12] & 127) / 100,
            'thickness': (_bytes[12] >> 7) | ((_bytes[13] & 15) << 1),
            'draw_outline': (_bytes[13] >> 4) & 3,
            '_screen_height': _bytes[2] | (_bytes[3] << 8)
        }

    def encode(self) -> str:
        """
        Translates a Crosshair object into a crosshair share code.

        Returns:
            A crosshair share code.
        """
        _bytes = self._get_bytes()
        num = int(_bytes.hex(), 16)

        code = ''
        for _ in range(25):
            num, r = divmod(num, DICTIONARY_LENGTH)
            code += DICTIONARY[r]

        return f'CSGO-{code[:5]}-{code[5:10]}-{code[10:15]}-{code[15:20]}-{code[20:]}'

    def _get_bytes(self):
        bytes_array = bytearray([
            0,
            3,
            ((self.style & 7) | (self.recoil << 4) | (self.dot << 6) | (self.t << 7)),
            self.red,
            self.green,
            self.blue,
            self.alpha,
            self.gap,
            self.length,
            self.dynamic_spread_limit,
            self.dynamic_splitdist & 127,
            (int(self.dynamic_splitalpha_innermod * 10) & 127) |
            ((int((self.dynamic_splitalpha_outermod - 0.3) * 20) & 1) << 7),
            (int(self.dynamic_maxdist_split_ratio * 100) & 127) | ((self.thickness & 1) << 7),
            ((self.thickness >> 1) & 15) | ((self.draw_outline & 3) << 4),
            self._screen_height & 255,
            (self._screen_height >> 8) & 255,
            0,
            0,
        ])
        bytes_array[0] = sum(bytes_array[1:]) & 128

        return to_bytes(bytes_array)
