#!/usr/bin/env python

import unittest

import budget

class TestCategoryDefinition(unittest.TestCase):

    def test_treee_subnames(self):
        s = 'Alimentaire:Cantine,Courses,RestaurationRapide'
        c = budget.CategoryDefinition.from_string(s)
        self.assertEqual(c.name, 'Alimentaire')
        self.assertEqual(c.subnames, 
                         ['Cantine', 'Courses' ,'RestaurationRapide'])

    def test_zero_subnames_without_colon(self):
        s = 'Alimentaire'
        c = budget.CategoryDefinition.from_string(s)
        self.assertEqual(c.name, 'Alimentaire')
        self.assertEqual(c.subnames, []) 

    def test_zero_subnames_with_colon(self):
        s = 'Alimentaire:'
        c = budget.CategoryDefinition.from_string(s)
        self.assertEqual(c.name, 'Alimentaire')
        self.assertEqual(c.subnames, []) 

class TestCategory(unittest.TestCase):

    def test_with_subname(self):
        c = budget.Category.from_string('Alimentaire:Cantine')
        self.assertEqual(c.name, 'Alimentaire')
        self.assertEqual(c.subname, 'Cantine')

    def test_without_subname_without_colon(self):
        c = budget.Category.from_string('Alimentaire')
        self.assertEqual(c.name, 'Alimentaire')
        self.assertEqual(c.subname, None)

    def test_without_subname_with_colon(self):
        c = budget.Category.from_string('Alimentaire:')
        self.assertEqual(c.name, 'Alimentaire')
        self.assertEqual(c.subname, None)

    def test_equal(self):
        a = budget.Category('Alimentaire', 'Cantine')
        b = budget.Category('Alimentaire', 'Cantine')
        self.assertEqual(a, b)

    def test_not_equal(self):
        a = budget.Category('Alimentaire', 'Cantine')
        b = budget.Category('Alimentaire', 'Courses')
        self.assertNotEqual(a, b)


if __name__ == '__main__':
    unittest.main()
