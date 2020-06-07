from biobb_common.tools import test_fixtures as fx
from biobb_pmx.pmx.pmxgentop import Pmxgentop

class TestPmxgentopSingularity():
    def setUp(self):
        fx.test_setup(self, 'pmxgentop_singularity')

    def tearDown(self):
        fx.test_teardown(self)

    def test_pmxgentop_singularity(self):
        Pmxgentop(properties=self.properties, **self.paths).launch()
        assert fx.not_empty(self.paths['output_top_zip_path'])
        assert fx.equal(self.paths['output_top_zip_path'], self.paths['ref_output_top_zip_path'])
