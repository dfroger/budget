#!/usr/bin/env python

import time

import budget

class Transaction:
    date_format = "%Y/%m/%d"
    status_dict = {'*': 'validated', '+': 'payed'}

    def __init__(self, date, status, category, amount,
                 comments=None, line_idx=None):
        """
        :param: date : Day of the transaction
        :type date: time.struct_time

        :param status: the character '*' (validated) or '+' (payed)
        :type status: string

        :param category: Which category the transaction is
        :type category: budget.Category

        :param amount: Amount of the transaction
        :type amount: float

        :param comments: Comments on the transactions
        :type comments: string

        :param line_idx: Line index, when transactions are read from a file
        :type line_idx: int
        """

        self.date = date
        self.year = date.tm_year
        self.month = date.tm_mon
        self.day = date.tm_mday

        self.status = status
        self.category = category
        self.amount = amount
        self.comments = comments
        self.cumul = None
        self.line_idx = None

    def make_report(self):
        if self.comments:
            operation = "{category} ({comments})".format(
                              category = self.category.make_report(),
                              comments = self.comments,
                          )
        else:
            operation = self.category.make_report()

        s = "{date} {status} {operation:<45} {amount:+10.2f} {cumul:+10.2f}"
        return s.format(
            date = time.strftime("%Y/%m/%d",self.date),
            status = self.status if self.status else ' ',
            operation = operation,
            amount = self.amount,
            cumul = self.cumul,
            )

    @staticmethod
    def make_report_legend():
        s = "{:<10} S {:<45} {:>10} {:>10}"
        return s.format('DATE', 'OPERATION', 'AMOUNT', 'CUMUL')

    @classmethod
    def _parse_date(cls, words):
        date_str = words.pop(0)
        date = time.strptime(date_str, Transaction.date_format)
        return date

    @classmethod
    def _parse_status(cls, words):
        if words[0] in cls.status_dict.keys():
            return words.pop(0)
        else:
            return None

    @classmethod
    def _parse_category(cls, words):
        return budget.Category.from_string(words.pop(0))

    @classmethod
    def _parse_amount(cls, words):
        return float(words.pop(0))

    @classmethod
    def _parse_comments(cls, words):
        if words[0].startswith("("):
            words[0] = words[0][1:] # remove parentesis (
            comments = []
            while words:
                word = words.pop(0)
                if word.endswith(')'):
                    comments.append(word[:-1])
                    break
                else:
                    comments.append(word)
            else:
                raise ValueError("Unmatched parentesis for transation comment")
            return " ".join(comments)
        else:
            return None

    @classmethod
    def from_string(cls, s):
        words = s.split()
        date = cls._parse_date(words)
        status = cls._parse_status(words)
        category = cls._parse_category(words)
        comments = cls._parse_comments(words)
        amount = cls._parse_amount(words)
        assert words == []
        return Transaction(date, status, category, amount, comments=comments)
