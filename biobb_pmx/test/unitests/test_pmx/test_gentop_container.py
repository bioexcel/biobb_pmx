from biobb_common.tools import test_fixtures as fx
from biobb_pmx.pmx.gentop import Gentop

class TestGentopContainer():
    def setUp(self):
        fx.test_setup(self, 'gentop_container')

    def tearDown(self):
        pass
        #fx.test_teardown(self)

    def test_gentop_docker(self):
        Gentop(properties=self.properties, **self.paths).launch()
        assert fx.not_empty(self.paths['output_top_zip_path'])
        assert fx.equal(self.paths['output_top_zip_path'], self.paths['ref_output_top_zip_path'])