from biobb_common.tools import test_fixtures as fx
from biobb_pmx.pmx.pmxanalyse import pmxanalyse


class TestPmxanalyseSingularity:
    def setUp(self):
        fx.test_setup(self, 'pmxanalyse_singularity')

    def tearDown(self):
        fx.test_teardown(self)

    def test_pmxanalyse_singularity(self):
        pmxanalyse(properties=self.properties, **self.paths)
        assert fx.not_empty(self.paths['output_result_path'])
