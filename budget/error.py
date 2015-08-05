class BudgetError(Exception):
    pass

class BudgetSyntaxError(BudgetError):

    def __init__(self, line, iline):

        self.line = line
        self.iline = iline
        self.value = (line,iline)

    def __str__(self):

        return  "Line %i: Invalid syntax: '%s'" % (self.iline, self.line)
