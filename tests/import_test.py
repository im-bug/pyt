import ast
import os

from .base_test_case import BaseTestCase
from pyt.ast_helper import get_call_names_as_string
from pyt.project_handler import get_directory_modules, get_modules_and_packages


class ImportTest(BaseTestCase):
    def test_import(self):
        path = os.path.normpath('example/import_test_project/import.py')

        project_modules = get_modules_and_packages(os.path.dirname(path))
        local_modules = get_directory_modules(os.path.dirname(path))

        self.cfg_create_from_file(path, project_modules, local_modules)

        EXPECTED = ["Entry module",
                    "Module Entry A",
                    "Module Exit A",
                    "Module Entry A",
                    "Module Exit A",
                    "temp_1_s = 'str'",
                    "s = temp_1_s",
                    "Function Entry B",
                    "ret_B = s",
                    "Exit B",
                    "¤call_1 = ret_B",
                    "b = ¤call_1",
                    "save_2_b = b",
                    "temp_2_s = 'sss'",
                    "s = temp_2_s",
                    "Function Entry A.B",
                    "ret_A.B = s",
                    "Exit A.B",
                    "b = save_2_b",
                    "¤call_2 = ret_A.B",
                    "c = ¤call_2",
                    "Exit module"]

        for node, expected_label in zip(self.cfg.nodes, EXPECTED):
            self.assertEqual(node.label, expected_label)

    def test_import_as(self):
        path = os.path.normpath('example/import_test_project/import_as.py')

        project_modules = get_modules_and_packages(os.path.dirname(path))
        local_modules = get_directory_modules(os.path.dirname(path))

        self.cfg_create_from_file(path, project_modules, local_modules)

        EXPECTED = ["Entry module",
                    "Module Entry A",
                    "Module Exit A",
                    "Module Entry A",
                    "Module Exit A",
                    "temp_1_s = 'str'",
                    "s = temp_1_s",
                    "Function Entry B",
                    "ret_B = s",
                    "Exit B",
                    "¤call_1 = ret_B",
                    "b = ¤call_1",
                    "save_2_b = b",
                    "temp_2_s = 'sss'",
                    "s = temp_2_s",
                    "Function Entry A.B",
                    "ret_foo.B = s",
                    "Exit A.B",
                    "b = save_2_b",
                    "¤call_2 = ret_foo.B",
                    "c = ¤call_2",
                    "Exit module"]

        for node, expected_label in zip(self.cfg.nodes, EXPECTED):
            self.assertEqual(node.label, expected_label)

    def test_from_directory(self):
        file_path = os.path.normpath('example/import_test_project/from_directory.py')
        project_path = os.path.normpath('example/import_test_project')

        project_modules = get_modules_and_packages(project_path)
        local_modules = get_directory_modules(project_path)

        self.cfg_create_from_file(file_path, project_modules, local_modules)


        EXPECTED = ["Entry module",
                    "Module Entry bar",
                    "Module Exit bar",
                    "temp_1_s = 'hey'",
                    "s = temp_1_s",
                    "Function Entry bar.H",
                    "ret_bar.H = s + 'end'",
                    "Exit bar.H",
                    "¤call_1 = ret_bar.H",
                    "Exit module"]

        for node, expected_label in zip(self.cfg.nodes, EXPECTED):
            self.assertEqual(node.label, expected_label)

    def test_relative_level_1(self):
        path = os.path.normpath('example/import_test_project/relative_level_1.py')

        project_modules = get_modules_and_packages(os.path.dirname(path))
        local_modules = get_directory_modules(os.path.dirname(path))

        self.cfg_create_from_file(path, project_modules, local_modules)

        EXPECTED = ["Entry module",
                    "Module Entry A",
                    "Module Exit A",
                    "Module Entry A",
                    "Module Exit A",
                    "temp_1_s = 'str'",
                    "s = temp_1_s",
                    "Function Entry B",
                    "ret_B = s",
                    "Exit B",
                    "¤call_1 = ret_B",
                    "b = ¤call_1",
                    "save_2_b = b",
                    "temp_2_s = 'sss'",
                    "s = temp_2_s",
                    "Function Entry A.B",
                    "ret_A.B = s",
                    "Exit A.B",
                    "b = save_2_b",
                    "¤call_2 = ret_A.B",
                    "c = ¤call_2",
                    "Exit module"]

        for node, expected_label in zip(self.cfg.nodes, EXPECTED):
            self.assertEqual(node.label, expected_label)

    def test_relative_level_2(self):
        path = os.path.normpath('example/import_test_project/relative_level_2.py')

        project_modules = get_modules_and_packages(os.path.dirname(path))
        local_modules = get_directory_modules(os.path.dirname(path))

        try:
            self.cfg_create_from_file(path, project_modules, local_modules)
        except Exception as e:
            self.assertTrue("OSError('Input needs to be a file. Path: " in repr(e))
            self.assertTrue("example/A.py" in repr(e))

    def test_relative_between_folders(self):
        file_path = os.path.normpath('example/import_test_project/other_dir/relative_between_folders.py')
        project_path = os.path.normpath('example/import_test_project')

        project_modules = get_modules_and_packages(project_path)
        local_modules = get_directory_modules(project_path)

        self.cfg_create_from_file(file_path, project_modules, local_modules)

        EXPECTED = ["Entry module",
                    "Module Entry foo.bar",
                    "Module Exit foo.bar",
                    "temp_1_s = 'hey'",
                    "s = temp_1_s",
                    "Function Entry H",
                    "ret_H = s + 'end'",
                    "Exit H",
                    "¤call_1 = ret_H",
                    "result = ¤call_1",
                    "Exit module"]

        for node, expected_label in zip(self.cfg.nodes, EXPECTED):
            self.assertEqual(node.label, expected_label)

    def test_relative_from_directory(self):
        file_path = os.path.normpath('example/import_test_project/relative_from_directory.py')
        project_path = os.path.normpath('example/import_test_project')

        project_modules = get_modules_and_packages(project_path)
        local_modules = get_directory_modules(project_path)

        self.cfg_create_from_file(file_path, project_modules, local_modules)

        EXPECTED = ["Entry module",
                    "Module Entry bar",
                    "Module Exit bar",
                    "temp_1_s = 'hey'",
                    "s = temp_1_s",
                    "Function Entry bar.H",
                    "ret_bar.H = s + 'end'",
                    "Exit bar.H",
                    "¤call_1 = ret_bar.H",
                    "Exit module"]

        for node, expected_label in zip(self.cfg.nodes, EXPECTED):
            self.assertEqual(node.label, expected_label)

    def test_from_dot(self):
        file_path = os.path.normpath('example/import_test_project/from_dot.py')
        project_path = os.path.normpath('example/import_test_project')

        project_modules = get_modules_and_packages(project_path)
        local_modules = get_directory_modules(project_path)

        self.cfg_create_from_file(file_path, project_modules, local_modules)

        EXPECTED = ['Entry module',
                    'Module Entry A',
                    'Module Exit A',
                    'temp_1_s = \'sss\'',
                    's = temp_1_s',
                    'Function Entry A.B',
                    'ret_A.B = s',
                    'Exit A.B',
                    '¤call_1 = ret_A.B',
                    'c = ¤call_1',
                    'Exit module']


        for node, expected_label in zip(self.cfg.nodes, EXPECTED):
            self.assertEqual(node.label, expected_label)

    def test_from_dot_dot(self):
        file_path = os.path.normpath('example/import_test_project/other_dir/from_dot_dot.py')
        project_path = os.path.normpath('example/import_test_project')

        project_modules = get_modules_and_packages(project_path)
        local_modules = get_directory_modules(project_path)

        self.cfg_create_from_file(file_path, project_modules, local_modules)

        EXPECTED = ['Entry module',
                    'Module Entry A',
                    'Module Exit A',
                    'temp_1_s = \'sss\'',
                    's = temp_1_s',
                    'Function Entry A.B',
                    'ret_A.B = s',
                    'Exit A.B',
                    '¤call_1 = ret_A.B',
                    'c = ¤call_1',
                    'Exit module']


        for node, expected_label in zip(self.cfg.nodes, EXPECTED):
            self.assertEqual(node.label, expected_label)

    def test_multiple_files_with_aliases(self):
        file_path = os.path.normpath('example/import_test_project/multiple_files_with_aliases.py')
        project_path = os.path.normpath('example/import_test_project')

        project_modules = get_modules_and_packages(project_path)
        local_modules = get_directory_modules(project_path)

        self.cfg_create_from_file(file_path, project_modules, local_modules)

        EXPECTED = ["Entry module",
                    "Module Entry A",
                    "Module Exit A",
                    "Module Entry B",
                    "Module Exit B",
                    "Module Entry C",
                    "Module Exit C",
                    "Module Entry D",
                    "Module Exit D",
                    "temp_1_s = 'tlayuda'",
                    "s = temp_1_s",
                    "Function Entry A.cosme",
                    "ret_A.cosme = s + 'aaa'",
                    "Exit A.cosme",
                    "¤call_1 = ret_A.cosme",
                    "a = ¤call_1",
                    "save_2_a = a",
                    "temp_2_s = 'mutton'",
                    "s = temp_2_s",
                    "Function Entry B.foo",
                    "ret_keens.foo = s + 'bee'",
                    "Exit B.foo",
                    "a = save_2_a",
                    "¤call_2 = ret_keens.foo",
                    "b = ¤call_2",
                    "save_3_a = a",
                    "save_3_b = b",
                    "temp_3_s = 'tasting'",
                    "s = temp_3_s",
                    "Function Entry C.foo",
                    "ret_per_se.foo = s + 'see'",
                    "Exit C.foo",
                    "a = save_3_a",
                    "b = save_3_b",
                    "¤call_3 = ret_per_se.foo",
                    "c = ¤call_3",
                    "save_4_a = a",
                    "save_4_b = b",
                    "save_4_c = c",
                    "temp_4_s = 'peking'",
                    "s = temp_4_s",
                    "Function Entry D.foo",
                    "ret_duck_house.foo = s + 'dee'",
                    "Exit D.foo",
                    "a = save_4_a",
                    "b = save_4_b",
                    "c = save_4_c",
                    "¤call_4 = ret_duck_house.foo",
                    "d = ¤call_4",
                    "Exit module"]

        for node, expected_label in zip(self.cfg.nodes, EXPECTED):
            self.assertEqual(node.label, expected_label)

    def test_multiple_functions_with_aliases(self):
        file_path = os.path.normpath('example/import_test_project/multiple_functions_with_aliases.py')
        project_path = os.path.normpath('example/import_test_project')

        project_modules = get_modules_and_packages(project_path)
        local_modules = get_directory_modules(project_path)

        self.cfg_create_from_file(file_path, project_modules, local_modules)

        EXPECTED = ["Entry module",
                    "Module Entry A",
                    "Module Exit A",
                    "temp_1_s = 'mutton'",
                    "s = temp_1_s",
                    "Function Entry B",
                    "ret_keens = s",
                    "Exit B",
                    "¤call_1 = ret_keens",
                    "a = ¤call_1",
                    "save_2_a = a",
                    "temp_2_s = 'tasting'",
                    "s = temp_2_s",
                    "Function Entry C",
                    "ret_C = s + 'see'",
                    "Exit C",
                    "a = save_2_a",
                    "¤call_2 = ret_C",
                    "b = ¤call_2",
                    "save_3_a = a",
                    "save_3_b = b",
                    "temp_3_s = 'peking'",
                    "s = temp_3_s",
                    "Function Entry D",
                    "ret_duck_house = s + 'dee'",
                    "Exit D",
                    "a = save_3_a",
                    "b = save_3_b",
                    "¤call_3 = ret_duck_house",
                    "c = ¤call_3",
                    "Exit module"]


        for node, expected_label in zip(self.cfg.nodes, EXPECTED):
            self.assertEqual(node.label, expected_label)

    # def test_init(self):
    #     file_path = os.path.normpath('example/import_test_project/init.py')
    #     project_path = os.path.normpath('example/import_test_project')

    #     project_modules = get_modules_and_packages(project_path)
    #     local_modules = get_directory_modules(project_path)

    #     self.cfg_create_from_file(file_path, project_modules, local_modules)

    #     EXPECTED = ['Not Yet']

    #     for node, expected_label in zip(self.cfg.nodes, EXPECTED):
    #         self.assertEqual(node.label, expected_label)

    # def test_all(self):
    #     file_path = os.path.normpath('example/import_test_project/all.py')
    #     project_path = os.path.normpath('example/import_test_project')

    #     project_modules = get_modules_and_packages(project_path)
    #     local_modules = get_directory_modules(project_path)

    #     self.cfg_create_from_file(file_path, project_modules, local_modules)

    #     EXPECTED = ['Not Yet']

    #     for node, expected_label in zip(self.cfg.nodes, EXPECTED):
    #         self.assertEqual(node.label, expected_label)

    # def test_no_all(self):
    #     file_path = os.path.normpath('example/import_test_project/no_all.py')
    #     project_path = os.path.normpath('example/import_test_project')

    #     project_modules = get_modules_and_packages(project_path)
    #     local_modules = get_directory_modules(project_path)

    #     self.cfg_create_from_file(file_path, project_modules, local_modules)

    #     EXPECTED = ['Not Yet']

    #     for node, expected_label in zip(self.cfg.nodes, EXPECTED):
    #         self.assertEqual(node.label, expected_label)

    def test_get_call_names_single(self):
        m = ast.parse('hi(a)')
        call = m.body[0].value

        result = get_call_names_as_string(call.func)

        self.assertEqual(result, 'hi')

    def test_get_call_names_uselesscase(self):
        m = ast.parse('defg.hi(a)')
        call = m.body[0].value

        result = get_call_names_as_string(call.func)

        self.assertEqual(result, 'defg.hi')

    def test_get_call_names_multi(self):
        m = ast.parse('abc.defg.hi(a)')
        call = m.body[0].value

        result = get_call_names_as_string(call.func)

        self.assertEqual(result, 'abc.defg.hi')
