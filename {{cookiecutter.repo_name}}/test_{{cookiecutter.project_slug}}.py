#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `pset_1` package."""

import os
import sys
from io import StringIO
from os import path
import xlsxwriter
from tempfile import TemporaryDirectory
from unittest import TestCase

from {{cookiecutter.project_slug}}.__main__ import excel_to_parquet
from {{cookiecutter.project_slug}}.__main__ import print_column_from_parquet
from {{cookiecutter.project_slug}}.hash_str import hash_str, get_user_id
from {{cookiecutter.project_slug}}.hash_str import get_csci_salt
from {{cookiecutter.project_slug}}.io import atomic_write, tempfile
from {{cookiecutter.project_slug}}.io import get_full_path


class FakeFileFailure(IOError):
    pass


class MainTest(TestCase):

    def setUp(self):
        self.held, sys.stdout = sys.stdout, StringIO()

    def test_excel_to_parquet(self):
        '''
        To test that an excel file is sucessfully converted to a parquet file.
        creates test.xlsx file, converts it to parquet file with the same name
        and then asserts true if the file exists.'''

        workbook = xlsxwriter.Workbook('test.xlsx')
        worksheet = workbook.add_worksheet()
        worksheet.write(0, 0, 'Test_Column')
        worksheet.write(1, 0, 'test_row')
        workbook.close()
        data_destination = get_full_path('test.xlsx')
        excel_to_parquet('test.xlsx', data_destination)
        self.assertEqual(True, path.exists(data_destination))
        os.remove(data_destination)
        os.remove('test.xlsx')


class HashTests(TestCase):
    def test_basic(self):
        self.assertEqual(hash_str("world!", salt="hello, ").hex()[:6],
                         "68e656")

    def test_get_csci_salt(self):
        '''Tests that salt in the environment variable can be read.
        Saves the original value first, sets a test value and then
        checks the return of the function. Finally sets the environment
        variable back to the original value.'''

        salt = str(os.getenv('CSCI_SALT'))
        os.environ['CSCI_SALT'] = '5389ff'
        self.assertEqual("b'S\\x89\\xff'", str(get_csci_salt()))
        os.environ['CSCI_SALT'] = salt

    def test_get_user_id(self):
        '''Tests that the get_user_id function returns
        the accurate hash for the provided id.'''

        salt = str(os.getenv('CSCI_SALT'))
        os.environ['CSCI_SALT'] = 'de3736'
        text = 'test'
        self.assertEqual('91e28b14', get_user_id(text))
        os.environ['CSCI_SALT'] = salt


class AtomicWriteTests(TestCase):
    def test_atomic_write(self):
        """Ensure file exists after being written successfully"""

        with TemporaryDirectory() as tmp:
            fp = os.path.join(tmp, "asdf.txt")

            with atomic_write(fp, "w") as f:
                assert not os.path.exists(fp)
                tmpfile = f.name
                f.write("asdf")

            assert not os.path.exists(tmpfile)
            assert os.path.exists(fp)

            with open(fp) as f:
                self.assertEqual(f.read(), "asdf")

    def test_atomic_failure(self):
        """Ensure that file does not exist after failure during write"""

        with TemporaryDirectory() as tmp:
            fp = os.path.join(tmp, "asdf.txt")

            with self.assertRaises(FakeFileFailure):
                with atomic_write(fp, "w") as f:
                    tmpfile = f.name
                    assert os.path.exists(tmpfile)
                    raise FakeFileFailure()

            assert not os.path.exists(tmpfile)
            assert not os.path.exists(fp)

    def test_file_exists(self):
        """Ensure an error is raised when a file exists"""

        if not os.path.exists('testfile'):
            with atomic_write('testfile', 'w') as f:
                f.write('this is a test')
        else:
            with self.assertRaises(FileExistsError):
                with atomic_write('testfile', 'w') as file:
                    file.write('this is a test')
        os.remove('testfile')

    def test_get_full_path(self):
        '''Build a full path with the given file name,
        and then check the get_full_path function
        against it to make sure the same path is returned.'''

        testfile_path = os.path.abspath(os.curdir) + "\\testfile.parquet"
        self.assertEqual(testfile_path, get_full_path('testfile'))

    def test_tempfile(self):
        '''Check temporary file is created in the context of the function,
        and then removed once the context is exited.'''
        with tempfile() as temp_file:
            self.assertEqual(True, path.exists(temp_file))

        self.assertEqual(False, path.exists(temp_file))

    def test_as_file_false(self):
        '''Test that if the as_file boolean is set to false,
        the return type is a string.'''

        with atomic_write('test', 'w', False) as f:
            self.assertIsInstance(f, str)
        os.remove('test')
