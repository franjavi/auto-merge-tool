import unittest
import merge
from sources.validation import Validator
from input_parameters import InputParameters


class ValidationTest(unittest.TestCase):

    def testMultilineMatch(self):
        validator = Validator()
        multiline = """* fia/-mergeToHtml5
      master
      remotes/origin/HEAD -> origin/master
      remotes/origin/Test/est
      remotes/origin/ah/th-1.4A
      remotes/origin/mothe/R53
      remotes/origin/rom_master"""

        self.assertTrue(validator.is_value_in_branches(multiline, "remotes/origin/" + "Test/HooksTest"))
        self.assertFalse(validator.is_value_in_branches(multiline, "remotes/origin/" + "Test1/HooksTest"))
        self.assertFalse(validator.is_value_in_branches(multiline, "remotes/origin/" + "HooksTest"))

    @unittest.skip
    def testValidateRemoteTA(self):
        validator = Validator()
        input_parameters = InputParameters()
        input_parameters.teamFork = """origin   http://sdfsdf@dsfsdfsd:7991/scm/ta/supom.git (fetch)
            origin   http://sdfsdf@dsfsdfsd:7991/scm/ta/supom.git (push)"""

        errors = []
        self.assertTrue(validator.validate_remotes(input_parameters.sourcesRoot, "supema", errors))

        input_parameters.teamFork = "origin   http://sdfsdf@dsfsdfsd:7991/scm/rata/super-poma.git (fetch)"
        errors = []
        self.assertFalse(validator.validate_remotes(input_parameters.sourcesRoot, "suppoma", errors))

    def testInputParametersValidateRemoteTA(self):
        validator = Validator()
        input_parameters = InputParameters()
        input_parameters.teamFork = "http://sdfsdf@dsfsdfsd:7991/scm/ta"
        validator.validate_input_parameters(input_parameters)
        self.assertEqual("", input_parameters.teamFork)

        input_parameters.teamFork = "http://sdfsdf@dsfsdfsd:7991/scm/rata"
        validator.validate_input_parameters(input_parameters)
        self.assertEqual("http://sdfsdf@dsfsdfsd:7991/scm/rata", input_parameters.teamFork)


if __name__ == '__main__':
    unittest.main()
