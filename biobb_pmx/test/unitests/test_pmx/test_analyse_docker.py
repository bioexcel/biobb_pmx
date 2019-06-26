from biobb_common.tools import test_fixtures as fx
from biobb_pmx.pmx.analyse import Analyse

class TestAnalyse():
    def setUp(self):
        fx.test_setup(self, 'analyse_docker')

    def tearDown(self):
        fx.test_teardown(self)

    def test_analyse_docker(self):
        Analyse(properties=self.properties, **self.paths).launch()
        assert fx.not_empty(self.paths['output_result_path'])
        #assert fx.equal(self.paths['output_result_path'], self.paths['ref_output_result_path'])
