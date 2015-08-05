#!/usr/bin/env python

class CategoryDefinition:

    def __init__(self,name,subnames):
        self.name = name
        self.subnames = subnames

    @staticmethod
    def from_string(s):
        """
        Parse string s and return a CategoryDefinition instance

        >>> s = 'Alimentaire:Cantine,Courses,RestaurationRapide'
        >>> category = CategoryDefinition.from_string(s)
        >>> print category.name
        Alimentaire
        print category.subname
        ['Catine', 'Courses', 'RestaurationRapide']
        """
        ncolons = s.count(':')
        if ncolons == 0:
            name = s
            subnames = []
        elif ncolons == 1:
            name, subnames = s.split(':')
            subnames = subnames.split(',') if subnames.strip() else []
        else:
            raise ValueError("Miss-formatted CategoryDefinition string: "\
                              "got %i colons" % (ncolons))
        return CategoryDefinition(name, subnames)

class Category:
    def __init__(self,name,subname=None):
        self.name = name
        self.subname = subname

    def __eq__(self, other):
        return self.name == other.name and self.subname == other.subname

    def __str__(self):
        return "<Category name=%s, subname=%s>" % (self.name, self.subname)

    def make_report(self):
        if self.subname:
            return self.name + ':' + self.subname
        else:
            return self.name

    @staticmethod
    def from_string(s):
        ncolons = s.count(':')
        if ncolons == 0:
            name = s
            subname = None
        elif ncolons == 1:
            name, subname = s.split(':')
            if not subname.strip():
                subname = None
        else:
            raise ValueError("Miss-formatted Category string: "\
                              "got %i colons" % (ncolons))
        return Category(name, subname)

if __name__ == '__main__':
    import doctest
    doctest.testmod()
