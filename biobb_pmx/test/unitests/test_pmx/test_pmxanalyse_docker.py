from biobb_common.tools import test_fixtures as fx
from biobb_pmx.pmxbiobb.pmxanalyse import pmxanalyse
# import pytest


class TestPmxanalyseDocker():
    def setup_class(self):
        fx.test_setup(self, 'pmxanalyse_docker')

    def teardown_class(self):
        fx.test_teardown(self)

    # @pytest.mark.skip(reason="Should add all the matplotlib functions")
    def test_pmxanalyse_docker(self):
        pmxanalyse(properties=self.properties, **self.paths)
        assert fx.not_empty(self.paths['output_result_path'])
