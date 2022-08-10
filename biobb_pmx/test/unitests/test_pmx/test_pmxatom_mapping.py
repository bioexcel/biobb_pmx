from biobb_common.tools import test_fixtures as fx
from biobb_pmx.pmx.pmxatom_mapping import pmxatom_mapping


class TestPmxatom_mapping:
    def setUp(self):
        fx.test_setup(self, 'pmxatom_mapping')

    def tearDown(self):
        fx.test_teardown(self)

    def test_pmxatom_mapping(self):
        pmxatom_mapping(properties=self.properties, **self.paths)
        assert fx.not_empty(self.paths['output_pairs1_path'])
        assert fx.not_empty(self.paths['output_pairs2_path'])
        assert fx.equal(self.paths['output_pairs1_path'], self.paths['ref_output_pairs1_path'])
        assert fx.equal(self.paths['output_pairs2_path'], self.paths['ref_output_pairs2_path'])

