#!/usr/bin/env python

import unittest

import budget

class TestTransaction(unittest.TestCase):

    def test_solde_initial(self):
        s = "2015/01/01 * SoldeInitial                          +8189.59"
        t = budget.Transaction.from_string(s)
        self.assertEqual(t.year, 2015)
        self.assertEqual(t.month, 1)
        self.assertEqual(t.day, 1)
        self.assertEqual(t.status, '*')
        self.assertEqual(t.category.name, 'SoldeInitial')
        self.assertEqual(t.category.subname, None)
        self.assertEqual(t.comments, None)
        self.assertEqual(t.amount, 8189.59)

    def test_comments(self):
        s = "2015/01/14 * Dons:Cadeaux (Anniversaire Carole)       -49.46"
        t = budget.Transaction.from_string(s)
        self.assertEqual(t.year, 2015)
        self.assertEqual(t.month, 1)
        self.assertEqual(t.day, 14)
        self.assertEqual(t.status, '*')
        self.assertEqual(t.category.name, 'Dons')
        self.assertEqual(t.category.subname, 'Cadeaux')
        self.assertEqual(t.comments, "Anniversaire Carole")
        self.assertEqual(t.amount, -49.46)

if __name__ == '__main__':
    unittest.main()
