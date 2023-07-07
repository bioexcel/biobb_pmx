from biobb_common.tools import test_fixtures as fx
from biobb_pmx.pmxbiobb.pmxmutate import pmxmutate


class TestPmxmutate:
    def setup_class(self):
        fx.test_setup(self, 'pmxmutate')

    def teardown_class(self):
        fx.test_teardown(self)

    def test_pmxmutate(self):
        pmxmutate(properties=self.properties, **self.paths)
        assert fx.not_empty(self.paths['output_structure_path'])
        assert fx.equal(self.paths['output_structure_path'], self.paths['ref_output_structure_path'])
