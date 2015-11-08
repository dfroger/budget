#!/usr/bin/env python

import unittest
import os
import time

import budget

here = os.path.realpath( os.path.dirname(__file__) )

class TestAccountLine(unittest.TestCase):

    def test_transaction(self):
        line = "2015/01/01 * SoldeInitial                          +8189.59\n"
        idx = 3
        account_line = budget.AccountLine(line, idx)
        self.assertFalse(account_line.is_comment)
        self.assertFalse(account_line.is_empty)
        self.assertEqual(account_line.line, line)
        self.assertEqual(account_line.idx, idx)

    def test_comment(self):
        line = "#==========================================================\n"
        idx = 9
        account_line = budget.AccountLine(line, idx)
        self.assertTrue(account_line.is_comment)
        self.assertFalse(account_line.is_empty)
        self.assertEqual(account_line.line, line)
        self.assertEqual(account_line.idx, idx)

    def test_empty(self):
        line = " \n"
        idx = 5
        account_line = budget.AccountLine(line, idx)
        self.assertFalse(account_line.is_comment)
        self.assertTrue(account_line.is_empty)
        self.assertEqual(account_line.line, line)
        self.assertEqual(account_line.idx, idx)

class TestAccount(unittest.TestCase):

    def setUp(self):
        self.filepath = os.path.join(here, 'example.budget')

    def test_read_lines(self):
        account_lines = budget.Account._read_lines(self.filepath)
        self.assertEqual(len(account_lines), 67)

    def test_from_file(self):
        b = budget.Account.from_file(self.filepath)
        self.assertEqual(len(b.category_definitions), 17)
        self.assertEqual(len(b.transactions), 50)
        self.assertEqual(len(b.categories), 42)

    def test_validate_categories(self):
        account_lines = budget.Account._read_lines(self.filepath)
        category_definitions, transactions = budget.Account._parse_lines(account_lines)
        transactions[10].category = budget.Category("Spaceship")
        msg="No such category: <Category name=Spaceship, subname=None>"
        self.assertRaisesRegex(AssertionError, msg, budget.Account,
                               category_definitions, transactions)

    def test_validate_dates(self):
        account_lines = budget.Account._read_lines(self.filepath)
        category_definitions, transactions = budget.Account._parse_lines(account_lines)
        transactions[10].date = time.strptime("2013/05/10", "%Y/%m/%d")
        msg = "Line 33, transaction date is older than previous one"
        self.assertRaisesRegex(ValueError, msg, budget.Account,
                               category_definitions, transactions)

    def test_make_report(self):
        self.maxDiff = None
        with open(os.path.join(here, 'example.report')) as f:
            expected_report = f.read()
        b = budget.Account.from_file(self.filepath)
        report = b.make_report()
        with open('got', 'w') as f:
            f.write(report)
        with open('ref', 'w') as f:
            f.write(expected_report)
        self.assertEqual(report, expected_report)

if __name__ == '__main__':
    unittest.main()
