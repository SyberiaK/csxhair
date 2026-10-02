from pathlib import Path

import pytest

from csxhair import Crosshair

N_CONFIGS = 30

CONVARS_TO_PARAMS = {
    "cl_crosshair_drawoutline": "draw_outline",
    "cl_crosshair_dynamic_maxdist_splitratio": "dynamic_maxdist_split_ratio",
    "cl_crosshair_dynamic_splitalpha_innermod": "dynamic_splitalpha_innermod",
    "cl_crosshair_dynamic_splitalpha_outermod": "dynamic_splitalpha_outermod",
    "cl_crosshair_dynamic_splitdist": "dynamic_splitdist",
    "cl_crosshair_dynamic_spread_limit": "dynamic_spread_limit",
    "cl_crosshair_gap": "gap",
    "cl_crosshair_length": "length",
    "cl_crosshair_recoil": "recoil",
    "cl_crosshair_t": "t",
    "cl_crosshair_thickness": "thickness",
    "cl_crosshaircolor_a": "alpha",
    "cl_crosshaircolor_b": "blue",
    "cl_crosshaircolor_g": "green",
    "cl_crosshaircolor_r": "red",
    "cl_crosshairdot": "dot",
    "cl_crosshairoutline_a": "outline_alpha",
    "cl_crosshairoutline_b": "outline_blue",
    "cl_crosshairoutline_g": "outline_green",
    "cl_crosshairoutline_r": "outline_red",
    "cl_crosshairstyle": "style",
    "cl_ironsight_usecrosshaircolor": "ironsight_usecrosshaircolor",
    "cl_ironsight_dot_scale": "ironsight_dot_scale",
}


def safe_eval(v: str):
    if v in ['true', 'false']:
        return v == 'true'
    if '.' in v:
        return float(v)
    if v.isdigit() or (v.startswith('-') and v[1:].isdigit()):
        return int(v)
    return v


def read_data_from_files(n: int):
    with open(Path(__file__).parent / f'crosshairs/{n}.cfg') as f:
        lines = [line.split() for line in f]
        params = {CONVARS_TO_PARAMS.get(k, k): safe_eval(v) for k, v in lines}
        code = params.pop('$code')
        x = Crosshair(**params)

    return code, x


def decode_check(code: str, expected: Crosshair):
    decoded = Crosshair.decode(code)
    mismatches = []

    for parameter in CONVARS_TO_PARAMS.values():
        actual = getattr(decoded, parameter)
        expected_value = getattr(expected, parameter)

        if actual != expected_value:
            mismatches.append(
                f"{parameter}: decoded={actual!r}, expected={expected_value!r}"
            )

    assert not mismatches, "Crosshair mismatch:\n" + "\n".join(mismatches)


@pytest.mark.parametrize("n", range(1, N_CONFIGS + 1))
def test_decode(n: int):
    decode_check(*read_data_from_files(n))
