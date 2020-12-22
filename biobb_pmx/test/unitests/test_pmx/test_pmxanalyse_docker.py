from biobb_common.tools import test_fixtures as fx
from biobb_pmx.pmx.pmxanalyse import pmxanalyse


class TestPmxanalyseDocker():
    def setUp(self):
        fx.test_setup(self, 'pmxanalyse_docker')

    def tearDown(self):
        fx.test_teardown(self)

    def test_pmxanalyse_docker(self):
        pmxanalyse(properties=self.properties, **self.paths)
        assert fx.not_empty(self.paths['output_result_path'])
