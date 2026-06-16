import ebtools
import ebtools.general as general


def test_sp_efa_functions_are_exported_from_general_namespace():
    assert general.sp_to_efa(47) == 1
    assert general.hour_to_efa(23) == 1


def test_sp_efa_functions_are_exported_from_top_level_namespace():
    assert ebtools.sp_to_efa(47) == 1
    assert ebtools.hour_to_efa(23) == 1
