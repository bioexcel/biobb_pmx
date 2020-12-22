from biobb_common.tools import test_fixtures as fx
from biobb_pmx.pmx.pmxgentop import pmxgentop


class TestPmxgentop:
    def setUp(self):
        fx.test_setup(self, 'pmxgentop')

    def tearDown(self):
        fx.test_teardown(self)

    def test_pmxgentop(self):
        pmxgentop(properties=self.properties, **self.paths)
        assert fx.not_empty(self.paths['output_top_zip_path'])
