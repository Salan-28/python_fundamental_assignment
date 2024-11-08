a1 = int
a2 = int
b1 = float
b2 = float
c1 = str
c2 = str
d1 = bool
d2 = bool


""" Opreartions on the variables """
a1=15
a2= 4
print(f"The sum of {a1} and {a2} is {a1+a2}")

b1=2.53
b2=3.54
print(f"The sum of {b1} and {b2} is {b1+b2}")

c1=" salan"
c2="hero"
print(c2+c1)

d1 = True
d2 = False

and_op= b1 and b2
or_op= b1 or b2


"""Dictionary to store their variables by their types as keys  
    e.g., int[10,20]
"""

dict={
    "int":[a1, a2],
    "float":[b1,b2],
    "str":[c1,c2],
    "bool":[b1,b2,and_op,or_op]
}

print("\nThe data in the dictionary are:")
for data_type, values in dict.items():
    print(f"{data_type}: {values}")