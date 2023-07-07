from biobb_common.tools import test_fixtures as fx
from biobb_pmx.pmxbiobb.pmxligand_hybrid import pmxligand_hybrid


class TestPmxligand_hybrid:
    def setup_class(self):
        fx.test_setup(self, 'pmxligand_hybrid')

    def teardown_class(self):
        fx.test_teardown(self)

    def test_pmxligand_hybrid(self):
        pmxligand_hybrid(properties=self.properties, **self.paths)
        assert fx.not_empty(self.paths['output_structure1_path'])
        assert fx.not_empty(self.paths['output_structure2_path'])
        assert fx.not_empty(self.paths['output_topology_path'])
        assert fx.not_empty(self.paths['output_atomtypes_path'])
        assert fx.equal(self.paths['output_structure1_path'], self.paths['ref_output_structure1_path'])
        assert fx.equal(self.paths['output_structure2_path'], self.paths['ref_output_structure2_path'])
        assert fx.equal(self.paths['output_topology_path'], self.paths['ref_output_topology_path'])
        assert fx.equal(self.paths['output_atomtypes_path'], self.paths['ref_output_atomtypes_path'])
