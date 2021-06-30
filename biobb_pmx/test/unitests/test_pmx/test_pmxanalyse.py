from biobb_common.tools import test_fixtures as fx
from biobb_pmx.pmx.pmxanalyse import pmxanalyse


class TestPmxanalyse:
    def setUp(self):
        fx.test_setup(self, 'pmxanalyse')

    def tearDown(self):
        #pass
        fx.test_teardown(self)

    def test_pmxanalyse(self):
        pmxanalyse(properties=self.properties, **self.paths)
        assert fx.not_empty(self.paths['output_result_path'])
        assert fx.not_empty(self.paths['output_work_plot_path'])
        assert fx.equal(self.paths['output_work_plot_path'], self.paths['ref_output_work_plot_path'])
