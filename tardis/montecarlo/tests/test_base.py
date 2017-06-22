import os
import pandas as pd
import numpy as np
import pytest
from astropy import units as u
from numpy.testing import assert_almost_equal
from tardis.io.config_reader import Configuration
from tardis.model import Radial1DModel
from tardis.montecarlo import MontecarloRunner


###
# Save and Load
###

@pytest.fixture(scope="module", autouse=True)
def to_hdf_buffer(hdf_file_path, simulation_verysimple):
    simulation_verysimple.runner.to_hdf(hdf_file_path, name='runner')

runner_properties = ['output_nu', 'output_energy', 'nu_bar_estimator',
                     'j_estimator', 'montecarlo_virtual_luminosity',
                     'last_interaction_in_nu',
                     'last_line_interaction_in_id',
                     'last_line_interaction_out_id',
                     'last_line_interaction_shell_id',
                     'packet_luminosity']

@pytest.mark.parametrize("attr", runner_properties)
def test_hdf_runner(hdf_file_path, simulation_verysimple, attr):
    actual_property = getattr(simulation_verysimple.runner, attr)
    if hasattr(actual_property, 'cgs'):
        actual_property = actual_property.cgs.value
    path = os.path.join('runner', attr)
    expected = pd.read_hdf(hdf_file_path, path)
    assert_almost_equal(actual_property, expected.values)
