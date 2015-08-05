#!/usr/bin/env python

import time

import budget

class AccountLine:

    comment_char = '#'

    def __init__(self,line, idx):
        self.line = line
        self.idx = idx
        self.stripped = self.line.strip()
        self.is_comment = self.stripped and \
                          self.stripped[0] == AccountLine.comment_char
        self.is_empty = line.strip() == ''
        self.words = self.line.split()

class Account:

    def __init__(self, category_definitions, transactions):
        self.category_definitions = category_definitions
        self.transactions = transactions
        self.categories = Account._compute_categories(self.category_definitions)
        self._validate_categories()
        self._validate_dates()
        self._compute_cumuls()

    def _validate_categories(self):
        for t in self.transactions:
            assert t.category in self.categories, "No such category: %s" % t.category

    def _validate_dates(self):
        for i in range(1, len(self.transactions)):
            if self.transactions[i].date < self.transactions[i-1].date:
                raise ValueError("Line %i, transaction date is older "
                                 "than previous one" % self.transactions[i].line_idx)

    def _compute_cumuls(self):
        first = self.transactions[0]
        first.cumul = first.amount

        for i in range(1, len(self.transactions)):
            self.transactions[i].cumul = self.transactions[i-1].cumul \
                                       + self.transactions[i].amount

    def make_report(self):
        def add_month_lines(lines, transaction, first=False):
            if not first:
                lines.append('')
            lines.append( time.strftime(" %B ",transaction.date).center(80,"=") )
            lines.append( budget.Transaction.make_report_legend() )

        lines = [ ]
        nfull = 0
        current_month = self.transactions[0].month
        add_month_lines(lines, self.transactions[0], first=True)
        for t in self.transactions:
            if t.month != current_month:
                add_month_lines(lines, t)
                current_month = t.month
            lines.append( t.make_report() )
            nfull += 1
            if nfull == 5:
                lines.append('')
                nfull = 0
        lines.append('')
        return '\n'.join(lines)

    @staticmethod
    def _compute_categories(category_definitions):
        categories = []
        for d in category_definitions:
            categories.append( budget.Category(d.name) )
            for subname in d.subnames:
                categories.append( budget.Category(d.name, subname) )
        return categories

    @staticmethod
    def _read_lines(filename):
        account_lines = []
        with open(filename) as f:
            for idx, line in enumerate(f):
                account_line = AccountLine(line, idx+1)
                if account_line.is_comment or account_line.is_empty:
                    pass
                else:
                    account_lines.append( account_line )
        return account_lines

    @staticmethod
    def _parse_category_definitions(account_lines):
        category_definitions = []
        while True:
            if len(account_lines[0].words) != 1:
                break
            else:
                s = account_lines.pop(0).stripped
                d = budget.CategoryDefinition.from_string(s)
                category_definitions.append(d)
        return category_definitions

    @staticmethod
    def _parse_transactions(account_lines):
        transactions = []
        for account_line in account_lines:
            t = budget.Transaction.from_string(account_line.stripped)
            t.line_idx = account_line.idx
            transactions.append(t)
        return transactions

    @classmethod
    def _parse_lines(cls, account_lines):
        category_definitions = cls._parse_category_definitions(account_lines)
        transactions = cls._parse_transactions(account_lines)
        return category_definitions, transactions

    @classmethod
    def from_file(cls, filename):
        account_lines = cls._read_lines(filename)
        category_definitions, transactions = cls._parse_lines(account_lines)
        return Account(category_definitions, transactions)
