from aegis_model.configs import AEGIS_1T_CONFIG, estimate_parameter_count, validate_1t_target


def test_aegis_1t_shape_and_count():
    assert AEGIS_1T_CONFIG.d_model == 16_384
    assert AEGIS_1T_CONFIG.n_layers == 320
    assert AEGIS_1T_CONFIG.n_heads == 128
    assert estimate_parameter_count(AEGIS_1T_CONFIG) == 1_031_954_006_016
    validate_1t_target()
