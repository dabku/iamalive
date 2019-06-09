import unittest
import json
from collections import OrderedDict
import os

from iamalive.helpers.server_helpers import create_token, hash_string, extract_properties_from_dict


class TestHelpersCommon(unittest.TestCase):

    def test_createtoken(self):
        for i in range(2, 30, 3):
            token = create_token(i)
            self.assertGreaterEqual(len(token), i)

    def test_hash_string(self):
        cases = [
            ('', b"\xe3\xb0\xc4B\x98\xfc\x1c\x14\x9a\xfb\xf4\xc8\x99o\xb9$'\xaeA\xe4d\x9b\x93L\xa4\x95\x99\x1bxR\xb8U"),
            ('Jh6J<6y', b"\t\x0b\xfd\xd9=\xfeo;\x16x\x1c\x195f\x032\xc65\n\x9d\x82V'\x82\xf5\x19\x80\xf9jl\xcf\xe2"),
            ('sVFL;]H_p4B<{3', b'(gU6~\x14L\x8a\xce\xc4L\x8d\xfe\x02Sw\xd0_\xf6\xea\x9c\x86M\x89\x8en\x00C\x1e~V\xfb'),
            ('}zS.a}*\tq62:f0\x0c1kMo@\x0b',
             b'S&\x1b\x14M\xff\xcc;\x10r\x90\x0c\x9a\x14\xd2\x7f\xd4\xc4TF\xb4:\xd1\x9dQ\xb3H\xe9\x9a\xe5p9'),
            ("H9e&\t?zl|dGJxD*}q>h:eBb\x0c|AX'",
             b'\xfd\x94\xc8L\xe2\x10\xec\xaf`4\xdbdb\x07\xbao\xb4*\xbbk\xc0L\x9c\xef\xb0$\xff\x19\xc6/\xf5\xad'),
            ("qV26\tHxhNvXCw\x0c*#Jik1gX5LnRVg?Kb'w~<",
             b'\x08u\xda\x98\xe1\xae\x86\x1a\xd5\x90\xb0a\xceA\x16\xdc,}^\x05E\x97\x1b\xb2\x19~\x96\xa91{\xb9\xa5')]
        for case_string, case_hash in cases:
            hashed = hash_string(case_string)
            self.assertEqual(hashed, case_hash)

    def test_extract_properties_from_dict(self):
        path_to_module = os.path.dirname(os.path.abspath(__file__))
        with open(os.path.join(path_to_module, 'test_data.json'), 'r') as f:
            test_cases = json.load(f, object_pairs_hook=OrderedDict)['test_extract_properties_from_dict']
        for _, case in test_cases.items():
            paths = extract_properties_from_dict(case['in'])
            col_paths = zip(paths, case['out'])
            for output_item, model_item in col_paths:
                self.assertDictEqual(output_item[1], model_item[1])
                self.assertEqual(output_item[0], model_item[0])
