import pprint
import traceback

import urllib.parse

import requests
from django.test import TestCase
from django.shortcuts import reverse
from django.conf import settings
from django.test import SimpleTestCase


class CreateStudentTestCase(SimpleTestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def setUp(self):
        # self.path = reverse('student-detail', kwargs={'pk': None}) # 这里不行
        self.path = 'api/v1/student'
        self.url = urllib.parse.urljoin(settings.HOST, self.path)
        self.headers = {}
        self.method = 'POST'
        self.data = {
            'name': '',
            'age': '',
            'gender': '',
        }

    def test_fetch(self):
        print('\033[0;36m{}\033[0m'.format(self.path))
        res = requests.request(method=self.method, url=self.url, json=self.data, headers=self.headers)
        try:
            pprint.pprint(res.json())
        except:
            print(res.content)

    def tearDown(self):
        pass
