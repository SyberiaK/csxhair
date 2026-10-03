from __future__ import annotations

from enum import IntEnum
from re import compile as re_compile
from sys import version_info

from attrs import Attribute, define, field

__version__ = '2.0.0'
__all__ = ['Crosshair']
__author__ = 'SyberiaK <syberiakey@gmail.com>'

ALPHABET = 'ABCDEFGHJKLMNOPQRSTUVWXYZabcdefhijkmnopqrstuvwxyz23456789'
ALPHABET_LENGTH = len(ALPHABET)
CODE_LENGTH = 44
CODE_PATTERN = re_compile(r'CS[{%s}]{%d}$' % (ALPHABET, CODE_LENGTH))

ColorInput = tuple[int, int, int] | tuple[int, int, int, int] | str

if version_info >= (3, 15):
    # noinspection PyUnresolvedReferences
    to_bytes = bytearray.take_bytes  # doesn't do a copy
else:
    to_bytes = bytes


def _lower_bool(x: bool, /) -> str:
    return str(x).lower()


def _hex_to_rgba(color: str) -> tuple[int, int, int, int]:
    if not isinstance(color, str):
        raise ValueError("Color must be a string")

    color = color.removeprefix("#")

    try:
        if len(color) == 3:
            r, g, b = (int(c * 2, 16) for c in color)
            return r, g, b, 255
        if len(color) == 6:
            r, g, b = (
                int(color[i:i + 2], 16)
                for i in (0, 2, 4)
            )
            return r, g, b, 255
        if len(color) == 8:
            r, g, b, a = (
                int(color[i:i + 2], 16)
                for i in (0, 2, 4, 6)
            )
            return r, g, b, a

        raise ValueError
    except ValueError:
        raise ValueError(f"Invalid HEX code: {color!r}") from None


def _parse_color(value: ColorInput) -> tuple[int, int, int, int]:
    if isinstance(value, tuple):
        if len(value) == 4:
            return value
        if len(value) == 3:
            r, g, b = value
            return r, g, b, 255
        raise ValueError(f"'{value}' is not a valid color.")

    if isinstance(value, str):
        return _hex_to_rgba(value)

    raise ValueError(f"'{value}' is not a valid color.")


def _validate_bounds(lower_bound: int | float, upper_bound: int | float, /):
    def inner(_, attribute: Attribute, value: int):
        if not (lower_bound <= value <= upper_bound):
            raise ValueError(f"'{attribute.name}' has to be in range [{lower_bound}; {upper_bound}] (found {value}).")

    return inner


def _round_float(_instance, _attribute, value: float) -> float:
    return round(value, 2)


class Style(IntEnum):
    DYNAMIC_CROSS = 0
    DYNAMIC_CIRCLE = 1
    DYNAMIC_CROSS_LEGACY = 2
    STATIC_CIRCLE = 3
    STATIC_CROSS = 4
    STATIC_CROSS_SHOT_FEEDBACK = 5
    DOT_ONLY = 6
    DYNAMIC_QUAD = 7
    STATIC_SQUARE = 8
    STATIC_QUAD = 9


class Outline(IntEnum):
    NONE = 0
    FULL = 1
    HALF = 2


@define
class Crosshair:
    """Represents a CS2 crosshair."""

    red: int = field(validator=_validate_bounds(0, 255))
    """
    ConVar: ``cl_crosshaircolor_r``

    [0; 255]
    """

    green: int = field(validator=_validate_bounds(0, 255))
    """
    ConVar: ``cl_crosshaircolor_g``

    [0; 255]
    """

    blue: int = field(validator=_validate_bounds(0, 255))
    """
    ConVar: ``cl_crosshaircolor_b``

    [0; 255]
    """

    alpha: int = field(validator=_validate_bounds(0, 255))
    """
    ConVar: ``cl_crosshaircolor_a``

    [0; 255]
    """

    recoil: bool = field(converter=bool)
    """
    ConVar: ``cl_crosshair_recoil``
    """

    draw_outline: Outline = field(converter=Outline, validator=_validate_bounds(0, 2))
    """
    ConVar: ``cl_crosshair_drawoutline``

    [0; 2]
    """

    outline_red: int = field(validator=_validate_bounds(0, 255))
    """
    ConVar: ``cl_crosshairoutline_r``

    [0; 255]
    """

    outline_green: int = field(validator=_validate_bounds(0, 255))
    """
    ConVar: ``cl_crosshairoutline_g``

    [0; 255]
    """

    outline_blue: int = field(validator=_validate_bounds(0, 255))
    """
    ConVar: ``cl_crosshairoutline_b``

    [0; 255]
    """

    outline_alpha: int = field(validator=_validate_bounds(0, 255))
    """
    ConVar: ``cl_crosshairoutline_a``

    [0; 255]
    """

    dynamic_splitdist: int = field(validator=_validate_bounds(0, 127))
    """
    ConVar: ``cl_crosshair_dynamic_splitdist``

    [0; 127]
    """

    dynamic_spread_limit: int = field(validator=_validate_bounds(0, 255))
    """
    ConVar: ``cl_crosshair_dynamic_spread_limit``

    [0; 255]
    """

    dynamic_splitalpha_innermod: float = field(validator=_validate_bounds(0, 1), on_setattr=_round_float)
    """
    ConVar: ``cl_crosshair_dynamic_splitalpha_innermod``

    [0.00; 1.00]
    """

    dynamic_splitalpha_outermod: float = field(validator=_validate_bounds(0.3, 1), on_setattr=_round_float)
    """
    ConVar: ``cl_crosshair_dynamic_splitalpha_outermod``

    [0.30; 1.00]
    """

    dynamic_maxdist_split_ratio: float = field(validator=_validate_bounds(0, 1), on_setattr=_round_float)
    """
    ConVar: ``cl_crosshair_dynamic_maxdist_splitratio``

    [0.00; 1.00]
    """

    thickness: int = field(validator=_validate_bounds(0, 32))
    """
    ConVar: ``cl_crosshair_thickness``

    [0; 32]
    """

    style: Style = field(converter=Style, validator=_validate_bounds(0, 9))
    """
    ConVar: ``cl_crosshairstyle``

    [0; 9]
    """

    dot: bool = field(converter=bool)
    """
    ConVar: ``cl_crosshairdot``
    """

    t: bool = field(converter=bool)
    """
    ConVar: ``cl_crosshair_t``
    """

    gap: int = field(validator=_validate_bounds(-3840, 3840))
    """
    ConVar: ``cl_crosshair_gap``

    [-3840; 3840]
    """

    length: int = field(validator=_validate_bounds(0, 255))
    """
    ConVar: ``cl_crosshair_length``

    [0; 255]
    """

    ironsight_usecrosshaircolor: bool = field(converter=bool)
    """
    ConVar: ``cl_ironsight_usecrosshaircolor``
    """

    ironsight_dot_scale: float = field(validator=_validate_bounds(0.1, 2), on_setattr=_round_float)
    """
    ConVar: ``cl_ironsight_dot_scale``

    [0.10; 2.00]
    """

    _screen_height: int = field(default=1080)
    """
    Stored in the crosshair code for compatibility sake.
    
    In most cases, it really just produces different share codes for the same crosshair.
    """

    @property
    def color(self) -> tuple[int, int, int, int]:
        return self.red, self.green, self.blue, self.alpha

    @color.setter
    def color(self, value: ColorInput, /):
        """
        Translates a passed value into crosshair's color properties.

        The valid values are:
        - ``tuple[int, int, int]``;
        - ``tuple[int, int, int, int]``;
        - ``str`` with a HEX code made with 3, 6 or 12 characters (e.g. ``"#fff"``, ``"#FAF0FAFF"``).

        Raises:
            ValueError: if the value can't be processed.
        """

        self.red, self.green, self.blue, self.alpha = _parse_color(value)

    @property
    def outline_color(self) -> tuple[int, int, int, int]:
        return self.outline_red, self.outline_green, self.outline_blue, self.outline_alpha

    @outline_color.setter
    def outline_color(self, value: ColorInput, /):
        """
        Translates a passed value into crosshair's outline color properties.

        The valid values are:
        - ``tuple[int, int, int]``;
        - ``tuple[int, int, int, int]``;
        - ``str`` with a HEX code made with 3, 6 or 12 characters (e.g. ``"#fff"``, ``"#FAF0FAFF"``).

        Raises:
            ValueError: if the value can't be processed.
        """

        self.outline_red, self.outline_green, self.outline_blue, self.outline_alpha = _parse_color(value)

    @property
    def convars(self) -> list[str]:
        """List of CS2's console variables to apply this crosshair."""

        return [
            f'cl_crosshair_drawoutline {self.draw_outline}',
            f'cl_crosshair_dynamic_maxdist_splitratio {self.dynamic_maxdist_split_ratio}',
            f'cl_crosshair_dynamic_splitalpha_innermod {self.dynamic_splitalpha_innermod}',
            f'cl_crosshair_dynamic_splitalpha_outermod {self.dynamic_splitalpha_outermod}',
            f'cl_crosshair_dynamic_splitdist {self.dynamic_splitdist}',
            f'cl_crosshair_dynamic_spread_limit {self.dynamic_spread_limit}',
            f'cl_crosshair_gap {self.gap}',
            f'cl_crosshair_length {self.length}'
            f'cl_crosshair_recoil {_lower_bool(self.recoil)}',
            f'cl_crosshair_t {_lower_bool(self.t)}',
            f'cl_crosshair_thickness {self.thickness}',
            f'cl_crosshaircolor_a {self.alpha}',
            f'cl_crosshaircolor_b {self.blue}',
            f'cl_crosshaircolor_g {self.green}',
            f'cl_crosshaircolor_r {self.red}',
            f'cl_crosshairdot {_lower_bool(self.dot)}',
            f'cl_crosshairoutline_a {self.outline_alpha}',
            f'cl_crosshairoutline_b {self.outline_blue}',
            f'cl_crosshairoutline_g {self.outline_green}',
            f'cl_crosshairoutline_r {self.outline_red}',
            f'cl_crosshairstyle {self.style}',
            f'cl_ironsight_usecrosshaircolor {_lower_bool(self.ironsight_usecrosshaircolor)}',
            f'cl_ironsight_dot_scale {self.ironsight_dot_scale}'
        ]

    @staticmethod
    def decode(code: str) -> Crosshair:
        """
        Translates a crosshair share code into a Crosshair object.

        Parameters:
            code (str):
                a crosshair share code (e.g. ``"CSjNcfcGjo8LLy2pDpCynr5e5efCGW6yXuf7B6aQ7wkWmU"``).

        Returns:
            a Crosshair object constructed from this code.

        Raises:
            ValueError: if the code is invalid.
        """

        if not CODE_PATTERN.match(code):
            raise ValueError(f"{code!r} doesn't match the pattern.")

        chars = code[2:]

        num = 0
        for c in reversed(chars):
            num = num * ALPHABET_LENGTH + ALPHABET.index(c)

        hexnum = hex(num)[2:].zfill(64)
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
        dyn = int.from_bytes(_bytes[18:22], "little")

        return {
            'screen_height': _bytes[2] | (_bytes[3] << 8),
            "style": _bytes[4] & 31,
            "recoil": bool(_bytes[4] & 32),
            "dot": bool(_bytes[4] & 64),
            "t": bool(_bytes[4] & 128),
            "red": _bytes[5],
            "green": _bytes[6],
            "blue": _bytes[7],
            "alpha": _bytes[8],
            "outline_red": _bytes[9],
            "outline_green": _bytes[10],
            "outline_blue": _bytes[11],
            "outline_alpha": _bytes[12],
            "thickness": _bytes[13] & 31,
            "draw_outline": (_bytes[13] >> 6) & 3,
            "gap": int.from_bytes(_bytes[14:16], "little", signed=True),
            "length": _bytes[16],
            "dynamic_spread_limit": _bytes[17] & 255,
            "dynamic_splitdist": _bytes[18] & 127,
            "dynamic_splitalpha_innermod": round(((dyn >> 7) & 127) / 100.0, 2),
            "dynamic_splitalpha_outermod": round(((dyn >> 14) & 127) / 100.0 + 0.3, 2),
            "dynamic_maxdist_split_ratio": round(((dyn >> 21) & 127) / 100.0, 2),
            "ironsight_usecrosshaircolor": bool(_bytes[21] & 16),
            "ironsight_dot_scale": 0.10 + _bytes[22] / 100,
        }

    def encode(self) -> str:
        """
        Translates a Crosshair object into a share code.

        Returns:
            A crosshair share code (e.g. ``"CSjNcfcGjo8LLy2pDpCynr5e5efCGW6yXuf7B6aQ7wkWmU"``).
        """

        num = int.from_bytes(self._get_bytes(), "big")

        code = 'CS'
        for _ in range(CODE_LENGTH):
            num, r = divmod(num, ALPHABET_LENGTH)
            code += ALPHABET[r]

        return code

    def _get_bytes(self):
        dyn = (
            (self.dynamic_splitdist & 127) |
            ((round(self.dynamic_splitalpha_innermod * 100) & 127) << 7) |
            ((round((self.dynamic_splitalpha_outermod - 0.3) * 100) & 127) << 14) |
            ((round(self.dynamic_maxdist_split_ratio * 100) & 127) << 21)
        )

        bytes_array = bytearray([
            0,
            1,
            *self._screen_height.to_bytes(2, "little"),
            (self.style & 31) | (int(self.recoil) << 5) | (int(self.dot) << 6) | (int(self.t) << 7),
            self.red,
            self.green,
            self.blue,
            self.alpha,
            self.outline_red,
            self.outline_green,
            self.outline_blue,
            self.outline_alpha,
            (self.thickness & 31) | ((self.draw_outline & 3) << 6),
            *self.gap.to_bytes(2, "little", signed=True),
            self.length,
            self.dynamic_spread_limit & 255,
            *dyn.to_bytes(4, "little"),
            round((self.ironsight_dot_scale - 0.10) * 100) & 255,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
        ])
        bytes_array[21] |= int(self.ironsight_usecrosshaircolor) << 4

        bytes_array[0] = sum(bytes_array[1:]) & 255
        return to_bytes(bytes_array)
