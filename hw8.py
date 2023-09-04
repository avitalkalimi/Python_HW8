# import copy


class Monom:
    def __init__(self, power, coef=1):
        self.power = power
        self.power = int(self.power)
        self.coef = coef
        self.next = None
        self.coef = round(self.coef, 2)
        if self.coef == int(self.coef):
            self.coef = int(self.coef)

    def __repr__(self):
        if self.coef < 0:  # for negative
            if self.power == 0:
                return "({A})".format(A=self.coef)
            if self.power == 1:
                    return "({A}{X})".format(A=self.coef, X = "X")
            return "({A}{X}^{B})".format(A = self.coef, X = "X", B = self.power)

        if self.coef == 0:  # for 0
            return "{A}".format(A = self.coef)
        if self.power == 0:
            return "{A}".format(A = self.coef)

        if self.power == 1:  # for 1
            if self.coef == 1:
                return "X"
            return "{A}{X}".format(A = self.coef, X = "X")
        if self.coef == 1:
            return "{X}^{B}".format(X = "X", B = self.power)

        else: return "{A}{X}^{B}".format(A = self.coef, X = "X", B = self.power)  # for normal

    def __mul__(self, other):
        if self.coef == 0:
            return 0
        if not isinstance(other, Monom):
            return Monom(self.power ,self.coef * other)
        else:
            return Monom(other.power + self.power ,other.coef * self.coef)

    def __rmul__(self, other):
        return self * other

    def derivative(self):
        return Monom(self.power - 1 ,self.power * self.coef)

    def integral(self):
        if self.coef == 0:
            return Monom(self.power ,self.coef)
        return Monom(self.power + 1 ,self.coef / (self.power+ 1))

    def __eq__(self, other):
        i = self
        u = other
        if i is None:
            if u is None:
                return True
            return False
        if u is None:
            return False
        return self.power == other.power and self.coef == other.coef
    def __gt__(self, other):
        i = self
        u = other
        if i is None:
            if u is None:
                return True
            return False
        if u is None:
            return True
        if self.power == other.power:
            return self.coef > other.coef
        return self.power > other.power
    def __le__(self, other):
        i = self
        u = other
        if i is None:
            if u is None:
                return True
            return True
        if u is None:
            return False
        if self.power == other.power:
            return self.coef <= other.coef
        return self.power <= other.power
    def __lt__(self, other):
        i = self
        u = other
        if i is None:
            if u is None:
                return False
            return True
        if u is None:
            return False
        if self.power == other.power:
            return self.coef < other.coef
        return self.power < other.power
    def __ge__(self, other):
        i = self
        u = other
        if i is None:
            if u is None:
                return True
            return False
        if u is None:
            return True
        if self.power == other.power:
            return self.coef >= other.coef
        return self.power >= other.power



class Polynomial(Monom):
    def __init__(self, l):
        self.head = None
        if type(l) != list:
            raise ValueError("Invalid polynomial initialization.")
        for i in l:
            if type(i) != tuple:
                raise ValueError("Invalid polynomial initialization.")
            if len(i) != 2:
                raise ValueError("Invalid polynomial initialization.")
            if type(i[0]) != int:
                if type(i[0]) != float:
                    raise ValueError("Invalid polynomial initialization.")
            if type(i[-1]) != int:
                if type(i[-1]) != float:
                    raise ValueError("Invalid polynomial initialization.")

        l = sorted(l, key=lambda x: (x[0], x[1]), reverse=True)
        i = 0
        while i < len(l) - 1:
            if l[i][0] == l[i + 1][0]:
                l.append((l[i][0], l[i][1] + l[i + 1][1]))
                l.remove(l[i])
                l.remove(l[i])
                l = sorted(l, key=lambda x: (x[0], x[1]), reverse=True)
                i = 0
            i += 1

        for i in range(len(l) - 1):
            if i >= len(l) -1:
                break
            if l[i][1] == 0:
                l.remove(l[i])

        for i in l:
            c = i[1]
            c = round(c, 2)
            if c != 0:
                self.insert_poly(i)

    def insert_poly(self, new_mono):
        new_mono = Monom(new_mono[0], new_mono[1])
        if self.head is None or new_mono > self.head:
            new_mono.next = self.head
            self.head = new_mono
        else:
            p = self.head
            while p.next is not None and p.next > new_mono:
                p = p.next
            new_mono.next = p.next
            p.next = new_mono

    def __repr__(self):
        mstr = "P(X)="
        p = self.head
        if p is None:
            return "P(X)=0"
        while p is not None:
            mstr += str(p) + "+"
            p = p.next

        return mstr[:-1]

    def rank(self):  # the rank of the poly
        if self.head is None:
            return 0
        else:
            mono = self.head
            return mono.power

    def calculate_value(self, x):  # sum the poly
        p = self.head
        s = 0
        while p is not None:
            s += (x ** p.power) * p.coef
            p = p.next
        return s

    def __neg__(self):  # cheng +- and return new poly
        p = self.head
        s = []
        while p is not None:
            s.append((p.power, p.coef * -1))
            p = p.next
        return Polynomial(s)

    def __sub__(self, other):
        other_poly = (other * -1)
        return self + other_poly

    def __add__(self, other):
        new_poly = []
        p = self.head
        q = other.head
        while p is not None:
            new_poly.append((p.power, p.coef))
            p = p.next
        while q is not None:
            new_poly.append((q.power, q.coef))
            q = q.next
        return Polynomial(new_poly)

    def __mul__(self, other):
        s = []
        p = self.head
        if not isinstance(other, Polynomial):
            while p is not None:
                s.append((p.power, p.coef * other))
                p = p.next
            return Polynomial(s)
        else:
            while p is not None:
                q = other.head
                while q is not None:
                    s.append((p.power + q.power, p.coef * q.coef))
                    q = q.next
                p = p.next
        return Polynomial(s)

    def __rmul__(self, other):
        return self * other

    def derivative(self):
        s = []
        p = self.head
        while p is not None:
            s.append((p.power - 1, p.power * p.coef))
            p = p.next
        return Polynomial(s)

    def integral(self, c=0):
        self.c = c
        s = []
        p = self.head
        while p is not None:
            s.append((p.power + 1,p.coef / (p.power + 1)))
            p = p.next
        s.append((0, c))
        return Polynomial(s)

    def __eq__(self, other):
        s = False
        self_len = 0
        other_len = 0
        p = self.head
        q = other.head
        if p is None and q is None:
            s = True
        while p is not None:
            p = p.next
            self_len += 1
        while q is not None:
            q = q.next
            other_len += 1
        if self_len  == other_len:
            i = self.head
            u = other.head
            for e in range(self_len):
                if i == u:
                    s = True
                else:
                    return False
                i = i.next
                u = u.next
        return s

    def __ge__(self, other):
        i = self.head
        u = other.head
        while i == u and i is not None and u is not None:
            i = i.next
            u = u.next
        if i is None:
            if u is None:
                return True
            return False
        if u is None:
            return True
        return i >= u

    def __gt__(self, other):
        i = self.head
        u = other.head
        while i == u and i is not None and u is not None:
            i = i.next
            u = u.next
        if i is None:
            if u is None:
                return False
            return False
        if u is None:
            return True
        return i > u

    def __lt__(self, other):
        i = self.head
        u = other.head
        while i == u and i is not None and u is not None:
            i = i.next
            u = u.next
        if i is None:
            if u is None:
                return False
            return True
        if u is None:
            return False
        return i < u

    def __le__(self, other):
        i = self.head
        u = other.head
        while i == u and i is not None and u is not None:
            i = i.next
            u = u.next
        if i is None:
            if u is None:
                return True
            return True
        if u is None:
            return False
        return i <= u

class BinTreeNode(Polynomial):  # class i get
    def __init__(self, polynomial):  # self = tree
        self.polynomial = polynomial
        self.left = self.right = None

    def is_leaf(self):
        return (self.left is None) and (self.right is None)

    def __repr__(self):
        return str(self.polynomial)

class PolynomialBST(BinTreeNode):  # class i write
    def __init__(self):
        self.head = None

    def insert(self, polynomial):  # insert node with val into tree, use recursion
        def insert_recursion(old_polynomial, new_polynomial):
            if new_polynomial <= old_polynomial.polynomial:
                if old_polynomial.left is None:
                    old_polynomial.left = BinTreeNode(new_polynomial)
                else:
                    insert_recursion(old_polynomial.left, new_polynomial)
            else:
                if old_polynomial.right is None:
                    old_polynomial.right = BinTreeNode(new_polynomial)
                else:
                    insert_recursion(old_polynomial.right, new_polynomial)

        if self.head is None:
            self.head = BinTreeNode(polynomial)
        else:
            insert_recursion(self.head, polynomial)

    def in_order(self):
        res = []
        def in_order_recursion(curr_node, res):
            if curr_node is not None:
                in_order_recursion(curr_node.left, res)
                res.append(curr_node.polynomial)
                in_order_recursion(curr_node.right, res)
            return res

        if self.head is None:  # empty tree
            return res
        else:
            return in_order_recursion(self.head, res)

    def __add__(self, other):
        new_tree = []
        self_list = self.in_order()
        other_list = other.in_order()
        for i in self_list:
            new_tree.append(i)
        for i in other_list:
            new_tree.append(i)
        new_tree_BST = PolynomialBST()
        for i in new_tree:
            new_tree_BST.insert(i)
        return new_tree_BST

p16= Polynomial([(5, 0.004)])
zero = Polynomial([])
print(p16)
print(zero)
print(p16.__eq__(zero))