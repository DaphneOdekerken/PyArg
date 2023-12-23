import json
import unittest

import requests


class TestToastAPI(unittest.TestCase):
    def test_toast_api(self):
        input_dict = {
            'premises': ['p', 'q'],
            'kbPrefs': ['p < q'],
            'rules': ['[r1] p => s', '[r2] q => t'],
            'rulePrefs': ['[r1]<[r2]'],
            'contrariness': ['s-t'],
            'link': 'weakest',
            'semantics': 'preferred',
            'assumptions': [],
            'axioms': []
        }
        json_str = json.dumps(input_dict)
        response = requests.post('http://toast.arg-tech.org/api/evaluate',
                                 json_str)
        result = response.json()
        self.assertEqual(len(result['arguments']), 4)
        self.assertListEqual(result['acceptableConclusions']['0'],
                             ['p', 'q', 't'])
