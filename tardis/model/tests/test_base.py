import os
import pytest
from astropy import units as u
from numpy.testing import assert_almost_equal, assert_array_almost_equal
import astropy.tests.helper as test_helper
from tardis.io.config_reader import Configuration
from tardis.model import Radial1DModel


def data_path(filename):
    return os.path.abspath(os.path.join('tardis/io/tests/data/', filename))


class TestModelFromPaper1Config:
    def setup(self):
        filename = 'paper1_tardis_configv1.yml'
        self.config = Configuration.from_yaml(data_path(filename))
        self.model = Radial1DModel.from_config(self.config)

    def test_abundances(self):
        oxygen_abundance = self.config.model.abundances.O
        assert_array_almost_equal(oxygen_abundance,
                                  self.model.abundance.ix[8].values)

    def test_velocities(self):
        velocity = self.config.model.structure.velocity
        assert_almost_equal(velocity.start.cgs.value,
                            self.model.v_inner[0].cgs.value)
        assert_almost_equal(velocity.stop.cgs.value,
                            self.model.v_outer[-1].cgs.value)
        assert len(self.model.v_outer) == velocity.num

    def test_densities(self):
        assert_almost_equal(self.model.density[0].cgs.value,
                            (7.542803599143591e-14 * u.Unit('g/cm^3')).value)
        assert_almost_equal(self.model.density[-1].cgs.value,
                            (1.432259798833509e-15 * u.Unit('g/cm^3')).value)

    def test_time_explosion(self):
        assert_almost_equal(self.model.time_explosion.to(u.day).value, 13.0)


class TestModelFromASCIIDensity:
    def setup(self):
        filename = 'tardis_configv1_ascii_density.yml'
        self.config = Configuration.from_yaml(data_path(filename))
        self.model = Radial1DModel.from_config(self.config)

    def test_velocities(self):
        assert self.model.v_inner.unit == u.Unit('cm/s')
        assert_almost_equal(self.model.v_inner[0].value, 1e4 * 1e5)

    def test_abundances(self):
        oxygen_abundance = self.config.model.abundances.O
        assert_array_almost_equal(oxygen_abundance,
                                  self.model.abundance.ix[8].values)


class TestModelFromArtisDensity:
    def setup(self):
        filename = 'tardis_configv1_artis_density.yml'
        self.config = Configuration.from_yaml(data_path(filename))
        self.model = Radial1DModel.from_config(self.config)

    def test_velocities(self):
        assert self.model.v_inner.unit == u.Unit('cm/s')
        assert_almost_equal(self.model.v_inner[0].value, 1.259375e+03 * 1e5)

    def test_abundances(self):
        oxygen_abundance = self.config.model.abundances.O
        assert_array_almost_equal(oxygen_abundance,
                                  self.model.abundance.ix[8].values)


class TestModelFromArtisDensityAbundances:
    def setup(self):
        filename = 'tardis_configv1_artis_density.yml'
        self.config = Configuration.from_yaml(data_path(filename))
        self.config.model.abundances.type = 'file'
        self.config.model.abundances.filename = 'artis_abundances.dat'
        self.config.model.abundances.filetype = 'artis'
        self.model = Radial1DModel.from_config(self.config)

    def test_velocities(self):
        assert self.model.v_inner.unit == u.Unit('cm/s')
        assert_almost_equal(self.model.v_inner[0].value, 1.259375e+03 * 1e5)

    def test_abundances(self):
        assert_almost_equal(self.model.abundance.ix[14, 54],
                            0.21864420000000001)


class TestModelFromArtisDensityAbundancesVSlice:
    def setup(self):
        filename = 'tardis_configv1_artis_density_v_slice.yml'
        self.config = Configuration.from_yaml(data_path(filename))
        self.config.model.abundances.type = 'file'
        self.config.model.abundances.filename = 'artis_abundances.dat'
        self.config.model.abundances.filetype = 'artis'
        self.model = Radial1DModel.from_config(self.config)

    def test_velocities(self):
        assert self.model.v_inner.unit == u.Unit('cm/s')
        assert_almost_equal(self.model.v_inner[0].to(u.km / u.s).value, 9000)

    def test_abundances(self):
        assert_almost_equal(self.model.abundance.ix[14, 31], 2.156751e-01)


class TestModelFromUniformDensity:
    def setup(self):
        filename = 'tardis_configv1_uniform_density.yml'
        self.config = Configuration.from_yaml(data_path(filename))
        self.model = Radial1DModel.from_config(self.config)

    def test_density(self):
        assert_array_almost_equal(self.model.density.to(u.Unit('g / cm3')).value,
                                  1.e-14)

class TestModelFromInitialTinner:
    def setup(self):
        filename = 'tardis_configv1_uniform_density.yml'
        self.config = Configuration.from_yaml(data_path(filename))
        self.config.plasma.initial_t_inner = 2508 * u.K
        self.model = Radial1DModel.from_config(self.config)

    def test_initial_temperature(self):
        assert_almost_equal(self.model.t_inner.value, 2508)


class TestModelFromArtisDensityAbundancesAllAscii:
    def setup(self):
        filename = 'tardis_configv1_ascii_density_abund.yml'
        self.config = Configuration.from_yaml(data_path(filename))
        self.config.model.structure.filename = 'density.dat'
        self.config.model.abundances.filename = 'abund.dat'
        self.model = Radial1DModel.from_config(self.config)

    def test_velocities(self):
        assert self.model.v_inner.unit == u.Unit('cm/s')
        assert_almost_equal(self.model.v_inner[0].to(u.km / u.s).value, 11000)

    def test_abundances(self):
        assert_almost_equal(self.model.abundance.ix[14, 0], 0.1)
        assert_almost_equal(self.model.abundance.ix[14, 1], 0.2)
        assert_almost_equal(self.model.abundance.ix[14, 2], 0.2)
        assert_almost_equal(self.model.abundance.ix[14, 3], 0.2)
        assert_almost_equal(self.model.abundance.ix[14, 4], 0.2)
        assert_almost_equal(self.model.abundance.ix[14, 5], 0.2)
        assert_almost_equal(self.model.abundance.ix[14, 6], 0.0)
        assert_almost_equal(self.model.abundance.ix[6, 0], 0.0)
        assert_almost_equal(self.model.abundance.ix[6, 1], 0.0)
        assert_almost_equal(self.model.abundance.ix[6, 2], 0.0)
        assert_almost_equal(self.model.abundance.ix[6, 3], 0.0)
        assert_almost_equal(self.model.abundance.ix[6, 4], 0.0)
        assert_almost_equal(self.model.abundance.ix[6, 5], 0.0)
        assert_almost_equal(self.model.abundance.ix[6, 6], 0.5)

    def test_densities(self):
        assert_almost_equal(self.model.density[0].to(u.Unit('g/cm3')).value, 9.7656229e-11 / 13.0**3)
        assert_almost_equal(self.model.density[1].to(u.Unit('g/cm3')).value, 4.8170911e-11 / 13.0**3)
        assert_almost_equal(self.model.density[2].to(u.Unit('g/cm3')).value, 2.5600000e-11 / 13.0**3)
        assert_almost_equal(self.model.density[3].to(u.Unit('g/cm3')).value, 1.4450533e-11 / 13.0**3)
        assert_almost_equal(self.model.density[4].to(u.Unit('g/cm3')).value, 8.5733893e-11 / 13.0**3)
        assert_almost_equal(self.model.density[5].to(u.Unit('g/cm3')).value, 5.3037103e-11 / 13.0**3)
        assert_almost_equal(self.model.density[6].to(u.Unit('g/cm3')).value, 3.3999447e-11 / 13.0**3)


def test_ascii_reader_power_law():
    filename = 'tardis_configv1_density_power_law_test.yml'
    config = Configuration.from_yaml(data_path(filename))
    model = Radial1DModel.from_config(config)

    expected_densites = [3.29072513e-14, 2.70357804e-14, 2.23776573e-14,
                         1.86501954e-14, 1.56435277e-14, 1.32001689e-14,
                         1.12007560e-14, 9.55397475e-15, 8.18935779e-15,
                         7.05208050e-15, 6.09916083e-15, 5.29665772e-15,
                         4.61758699e-15, 4.04035750e-15, 3.54758837e-15,
                         3.12520752e-15, 2.76175961e-15, 2.44787115e-15,
                         2.17583442e-15, 1.93928168e-15]

    assert model.no_of_shells == 20
    for i, mdens in enumerate(expected_densites):
        assert_almost_equal(model.density[i].to(u.Unit('g / (cm3)')).value,
                            mdens)


def test_ascii_reader_exponential_law():
    filename = 'tardis_configv1_density_exponential_test.yml'
    config = Configuration.from_yaml(data_path(filename))
    model = Radial1DModel.from_config(config)

    expected_densites = [5.18114795e-14, 4.45945537e-14, 3.83828881e-14,
                         3.30364579e-14, 2.84347428e-14, 2.44740100e-14,
                         2.10649756e-14, 1.81307925e-14, 1.56053177e-14,
                         1.34316215e-14, 1.15607037e-14, 9.95038990e-15,
                         8.56437996e-15, 7.37143014e-15, 6.34464872e-15,
                         5.46088976e-15, 4.70023138e-15, 4.04552664e-15,
                         3.48201705e-15, 2.99699985e-15]
    expected_unit = 'g / (cm3)'

    assert model.no_of_shells == 20
    for i, mdens in enumerate(expected_densites):
        assert_almost_equal(model.density[i].value, mdens)
        assert model.density[i].unit ==  u.Unit(expected_unit)

###
# Save and Load
###


@pytest.fixture(scope="module")
def hdf_file_path(tmpdir_factory):
    path = tmpdir_factory.mktemp('hdf_buffer').join('model.hdf')
    return str(path)


@pytest.fixture(scope="module")
def actual_model():
    filename = 'tardis_configv1_verysimple.yml'
    config = Configuration.from_yaml(data_path(filename))
    model = Radial1DModel.from_config(config)
    return model


@pytest.fixture(scope="module", autouse=True)
def to_hdf_buffer(hdf_file_path, actual_model):
    actual_model.to_hdf(hdf_file_path, 'model')


@pytest.fixture(scope="module")
def from_hdf_buffer(hdf_file_path):
    hdf_buffer = Radial1DModel.from_hdf(hdf_file_path, 'model')
    return hdf_buffer


model_quantity_attrs = ['luminosity_requested', 'time_explosion',
                        't_inner', 't_rad', 'v_inner', 'v_outer',
                        'velocity']


@pytest.mark.parametrize("attr", model_quantity_attrs)
def test_hdf_model_quantites(from_hdf_buffer, actual_model, attr):
    test_helper.assert_quantity_allclose(getattr(actual_model, attr), getattr(
        from_hdf_buffer, attr))


model_nparray_attrs = ['abundance', 'dilution_factor']


@pytest.mark.parametrize("attr", model_nparray_attrs)
def test_hdf_model_nparray(from_hdf_buffer, actual_model, attr):
    assert_array_almost_equal(getattr(actual_model, attr), getattr(
        from_hdf_buffer, attr))
