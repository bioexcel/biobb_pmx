from biobb_common.tools import test_fixtures as fx
from biobb_pmx.pmx.pmxmutate import pmxmutate


class TestPmxmutateDocker:
    def setUp(self):
        fx.test_setup(self, 'pmxmutate_docker')

    def tearDown(self):
        #pass
        fx.test_teardown(self)

    def test_pmxmutate_docker(self):
        pmxmutate(properties=self.properties, **self.paths)
        assert fx.not_empty(self.paths['output_structure_path'])
        assert fx.equal(self.paths['output_structure_path'], self.paths['ref_output_structure_path'])
