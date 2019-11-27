from biobb_common.tools import test_fixtures as fx
from biobb_pmx.pmx.mutate import Mutate

class TestMutateDocker():
    def setUp(self):
        fx.test_setup(self, 'mutate_container')

    def tearDown(self):
        fx.test_teardown(self)

    def test_mutate_container(self):
        Mutate(properties=self.properties, **self.paths).launch()
        assert fx.not_empty(self.paths['output_structure_path'])
        assert fx.equal(self.paths['output_structure_path'], self.paths['ref_output_structure_path'])
