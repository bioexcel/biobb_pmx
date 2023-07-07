from biobb_common.tools import test_fixtures as fx
from biobb_pmx.pmxbiobb.pmxanalyse import pmxanalyse
import pytest


class TestPmxanalyse:
    def setup_class(self):
        fx.test_setup(self, 'pmxanalyse')

    def teardown_class(self):
        # pass
        fx.test_teardown(self)

    # @pytest.mark.skip(reason="Should add all the matplotlib functions")
    def test_pmxanalyse(self):
        pmxanalyse(properties=self.properties, **self.paths)
        assert fx.not_empty(self.paths['output_result_path'])
        assert fx.not_empty(self.paths['output_work_plot_path'])
        assert fx.equal(self.paths['output_work_plot_path'], self.paths['ref_output_work_plot_path'])
