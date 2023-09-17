from biobb_common.tools import test_fixtures as fx
from biobb_pmx.pmxbiobb.pmxmerge_ff import pmxmerge_ff


class TestPmxmerge_ff:
    def setup_class(self):
        fx.test_setup(self, 'pmxmerge_ff')

    def teardown_class(self):
        fx.test_teardown(self)

    def test_pmxmerge_ff(self):
        pmxmerge_ff(properties=self.properties, **self.paths)
        assert fx.not_empty(self.paths['output_topology_path'])
        # Does not work in GitHub Actions
        # assert fx.equal(self.paths['output_topology_path'], self.paths['ref_output_topology_path'])
        fx.compare_size(self.paths['output_topology_path'], self.paths['ref_output_topology_path'])
