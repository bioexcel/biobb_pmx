from biobb_common.tools import test_fixtures as fx
from biobb_pmx.pmx.pmxcreate_top import pmxcreate_top


class TestPmxcreate_top:
    def setUp(self):
        fx.test_setup(self, 'pmxcreate_top')

    def tearDown(self):
        fx.test_teardown(self)

    def test_pmxcreate_top(self):
        pmxcreate_top(properties=self.properties, **self.paths)
        assert fx.not_empty(self.paths['output_topology_path'])
        assert fx.equal(self.paths['output_topology_path'], self.paths['ref_output_topology_path'])
