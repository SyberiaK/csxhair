from __future__ import annotations

import re

from attrs import define, field, validators

__version__ = '1.0.0'
__all__ = ('Crosshair',)

DICTIONARY = 'ABCDEFGHJKLMNOPQRSTUVWXYZabcdefhijkmnopqrstuvwxyz23456789'
DICTIONARY_LENGTH = len(DICTIONARY)
CODE_PATTERN = re.compile(r'CSGO(-[{%s}]{5}){5}$' % DICTIONARY)


def signed_byte(x, /) -> int:
    """Converts an unsigned byte to a signed one."""

    return (x ^ 0x80) - 0x80  # https://stackoverflow.com/a/37095855


def lowercase_bool(x, /) -> str:
    """For the sake of values unifying - returns a lowercase string of bool (``'True'`` -> ``'true'``)."""

    if type(x) is bool:
        return str(x).lower()

    raise ValueError(f'Expected bool, got {x}')


def _validate_bounds(lower_bound, upper_bound, /):
    def inner(_, attribute, value):
        if not (lower_bound <= value <= upper_bound):
            raise ValueError(f"'{attribute}' has to be in range [{lower_bound}; {upper_bound}].")

    return inner


@define
class Crosshair:
    """Represents a CS:GO/CS2 crosshair."""

    gap: float = field(validator=_validate_bounds(-12.8, 12.7))
    """
    Command: ``cl_crosshairgap``

    [-12.8; 12.7]
    """

    outline_thickness: float = field(validator=_validate_bounds(-0.0, 3.0))
    """
    Command: ``cl_crosshair_outlinethickness``

    [0.0; 3.0]
    """

    red: int = field(validator=_validate_bounds(0, 255))
    """
    Command: ``cl_crosshaircolor_r``

    [0; 255]

    Note:
        Applies only if ``Crosshair.color == 5``.
    """

    green: int = field(validator=_validate_bounds(0, 255))
    """
    Command: ``cl_crosshaircolor_g``

    [0; 255]

    Note:
        Applies only if ``Crosshair.color == 5``.
    """

    blue: int = field(validator=_validate_bounds(0, 255))
    """
    Command: ``cl_crosshaircolor_b``

    [0; 255]

    Note:
        Applies only if ``Crosshair.color == 5``.
    """

    alpha: int = field(validator=_validate_bounds(0, 255))
    """
    Command: ``cl_crosshairalpha``

    [0; 255]

    Note:
        Applies only if ``Crosshair.use_alpha == True``.
    """

    dynamic_splitdist: int = field(validator=_validate_bounds(0, 127))
    """
    Command: ``cl_crosshair_dynamic_splitdist``

    [0; 127]
    """

    recoil: bool = field(converter=bool)
    """
    Command: ``cl_crosshair_recoil``

    Note:
        This setting is exclusive to CS2, every crosshair imported from CS:GO have this value set to ``false``.
    """

    fixed_gap: float = field(validator=_validate_bounds(-12.8, 12.7))
    """
    Command: ``cl_fixedcrosshairgap``

    [-12.8; 12.7]
    """

    color: int = field(validator=validators.instance_of(int))
    """
    Command: ``cl_crosshaircolor``

    [0; 5]

    Note:
        0 - red (250, 50, 50) \n
        1 - green (50, 250, 50) \n
        2 - yellow (250, 250, 50) \n
        3 - blue (50, 50, 250) \n
        4 - cyan (50, 250, 250) \n
        5 - custom \n
        Any other values set green color (1).
    """

    draw_outline: bool = field(converter=bool)
    """
    Command: ``cl_crosshair_drawoutline``
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

    thickness: float = field(validator=_validate_bounds(0, 6.3))
    """
    Command: ``cl_crosshairthickness``

    [0.0; 6.3]
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

    gap_use_weapon_value: bool = field(converter=bool)
    """
    Command: ``cl_crosshairgap_useweaponvalue``
    """

    use_alpha: bool = field(converter=bool)
    """
    Command: ``cl_crosshairusealpha``
    """

    t: bool = field(converter=bool)
    """
    Command: ``cl_crosshair_t``
    """

    size: float = field(validator=_validate_bounds(0, 819.1))
    """
    Command: ``cl_crosshairsize``

    [0.0; 819.1]
    """

    @property
    def csgo_commands(self) -> list[str]:
        """List of commands to apply this crosshair in CS:GO."""

        return [
            f'cl_crosshairgap {self.gap}',
            f'cl_crosshair_outlinethickness {self.outline_thickness}',
            f'cl_crosshaircolor_r {self.red}',
            f'cl_crosshaircolor_g {self.green}',
            f'cl_crosshaircolor_b {self.blue}',
            f'cl_crosshairalpha {self.alpha}',
            f'cl_crosshair_dynamic_splitdist {self.dynamic_splitdist}',
            f'cl_fixedcrosshairgap {self.fixed_gap}',
            f'cl_crosshaircolor {self.color}',
            f'cl_crosshair_drawoutline {int(self.draw_outline)}',
            f'cl_crosshair_dynamic_splitalpha_innermod {self.dynamic_splitalpha_innermod}',
            f'cl_crosshair_dynamic_splitalpha_outermod {self.dynamic_splitalpha_outermod}',
            f'cl_crosshair_dynamic_maxdist_splitratio {self.dynamic_maxdist_split_ratio}',
            f'cl_crosshairthickness {self.thickness}',
            f'cl_crosshairstyle {self.style}',
            f'cl_crosshairdot {int(self.dot)}',
            f'cl_crosshairgap_useweaponvalue {int(self.gap_use_weapon_value)}',
            f'cl_crosshairusealpha {int(self.use_alpha)}',
            f'cl_crosshair_t {int(self.t)}',
            f'cl_crosshairsize {self.size}'
        ]

    @property
    def cs2_commands(self) -> list[str]:
        """List of commands to apply this crosshair in CS2."""

        return [
            f'cl_crosshairgap {self.gap}',
            f'cl_crosshair_outlinethickness {self.outline_thickness}',
            f'cl_crosshaircolor_r {self.red}',
            f'cl_crosshaircolor_g {self.green}',
            f'cl_crosshaircolor_b {self.blue}',
            f'cl_crosshairalpha {self.alpha}',
            f'cl_crosshair_dynamic_splitdist {self.dynamic_splitdist}',
            f'cl_crosshair_recoil {lowercase_bool(self.recoil)}',
            f'cl_fixedcrosshairgap {self.fixed_gap}',
            f'cl_crosshaircolor {self.color}',
            f'cl_crosshair_drawoutline {lowercase_bool(self.draw_outline)}',
            f'cl_crosshair_dynamic_splitalpha_innermod {self.dynamic_splitalpha_innermod}',
            f'cl_crosshair_dynamic_splitalpha_outermod {self.dynamic_splitalpha_outermod}',
            f'cl_crosshair_dynamic_maxdist_splitratio {self.dynamic_maxdist_split_ratio}',
            f'cl_crosshairthickness {self.thickness}',
            f'cl_crosshairstyle {self.style}',
            f'cl_crosshairdot {lowercase_bool(self.dot)}',
            f'cl_crosshairgap_useweaponvalue {lowercase_bool(self.gap_use_weapon_value)}',
            f'cl_crosshairusealpha {lowercase_bool(self.use_alpha)}',
            f'cl_crosshair_t {lowercase_bool(self.t)}',
            f'cl_crosshairsize {self.size}'
        ]

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
            'gap': signed_byte(_bytes[2]) / 10,
            'outline_thickness': _bytes[3] / 2,
            'red': _bytes[4],
            'green': _bytes[5],
            'blue': _bytes[6],
            'alpha': _bytes[7],
            'dynamic_splitdist': _bytes[8] & 0x7f,
            'recoil': ((_bytes[8] >> 4) & 8) == 8,
            'fixed_gap': signed_byte(_bytes[9]) / 10,
            'color': _bytes[10] & 7,
            'draw_outline': (_bytes[10] & 8) == 8,
            'dynamic_splitalpha_innermod': (_bytes[10] >> 4) / 10,
            'dynamic_splitalpha_outermod': (_bytes[11] & 0xf) / 10,
            'dynamic_maxdist_split_ratio': (_bytes[11] >> 4) / 10,
            'thickness': _bytes[12] / 10,
            'style': (_bytes[13] & 0xf) >> 1,
            'dot': ((_bytes[13] >> 4) & 1) == 1,
            'gap_use_weapon_value': ((_bytes[13] >> 4) & 2) == 2,
            'use_alpha': ((_bytes[13] >> 4) & 4) == 4,
            't': ((_bytes[13] >> 4) & 8) == 8,
            'size': (((_bytes[15] & 0x1f) << 8) + _bytes[14]) / 10
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
        bytes_array = [
            0,
            1,
            int(self.gap * 10) & 0xff,
            int(self.outline_thickness * 2),
            self.red,
            self.green,
            self.blue,
            self.alpha,
            self.dynamic_splitdist | (int(self.recoil) << 7),
            int(self.fixed_gap * 10) & 0xff,
            (self.color & 7) | (int(self.draw_outline) << 3) | (int(self.dynamic_splitalpha_innermod * 10) << 4),
            int(self.dynamic_splitalpha_outermod * 10) | (int(self.dynamic_maxdist_split_ratio * 10) << 4),
            int(self.thickness * 10),
            (self.style << 1) |
            (int(self.dot) << 4) |
            (int(self.gap_use_weapon_value) << 5) |
            (int(self.use_alpha) << 6) |
            (int(self.t) << 7),
            int(self.size * 10) & 0xff,
            (int(self.size * 10) >> 8) & 0x1f,
            0,
            0
        ]
        bytes_array[0] = sum(bytes_array) & 0xff

        return bytes(bytes_array)
