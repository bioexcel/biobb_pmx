from biobb_common.tools import test_fixtures as fx
from biobb_pmx.pmx.pmxanalyse import Pmxanalyse

class TestPmxanalyseDocker():
    def setUp(self):
        fx.test_setup(self, 'pmxanalyse_docker')

    def tearDown(self):
        fx.test_teardown(self)

    def test_pmxanalyse_docker(self):
        Pmxanalyse(properties=self.properties, **self.paths).launch()
        assert fx.not_empty(self.paths['output_result_path'])
        #assert fx.equal(self.paths['output_result_path'], self.paths['ref_output_result_path'])
