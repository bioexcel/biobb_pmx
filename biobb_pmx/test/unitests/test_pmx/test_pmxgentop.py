# type: ignore
from biobb_common.tools import test_fixtures as fx
from biobb_pmx.pmxbiobb.pmxgentop import pmxgentop


class TestPmxgentop:
    def setup_class(self):
        fx.test_setup(self, 'pmxgentop')

    def teardown_class(self):
        fx.test_teardown(self)
        # pass

    def test_pmxgentop(self):
        pmxgentop(properties=self.properties, **self.paths)
        assert fx.not_empty(self.paths['output_top_zip_path'])
        assert fx.equal(self.paths['output_top_zip_path'], self.paths['ref_output_top_zip_path'])
