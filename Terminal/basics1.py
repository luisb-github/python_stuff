print("")
# fundamental Data Types (int, float, bool str, list, tupple, set, dict)
print("\n Fundamental Data Types")
print("-----------------------\n")
print(type(6))
print(type(2 - 4))
print(type(2 * 4))
print(type(2 / 4))

print("\n Operators")
print("-----------------------\n")
print(2 ** 3) #expoente
print(5 // 4) # arredonda para baixo
print(5 % 4) # apresenta o resto da divisão

print("\n Math Functions")
print("-----------------------\n")
print(round(3.9)) #arredonda o numero para o mais proximo
print(abs(-20)) #da o valor absoluto sem sinais

# python segue a ordem correta de fazer as contas:
# ()
# **
# * /
# + -

print("\n Binary")
print("-----------------------\n")
print(bin(5)) # aprenseta o binario do numero
print(int('0b101', 2)) # apresenta o int de um binario(2) ou hexadecimal(16)

print("\n Variables")
print("-----------------------\n")

# naming variables best practices :
# use snake_case
# start with lowercase or underscore
# if you use underscore it means it is a private var, is still a normal var
# full caps var it means it is a Constant
# you can use letters, numbers, underscores
# is case sensitive
# dont overwrite keywords that already exist on python

user_age = 44
print(user_age)

#multiple vars
a,b,c = 1,2,3
print(a)
print(b)
print(c)

print("\n Expression vs Statements")
print("-----------------------\n")

print("iq = 5 -> Statement")
print("it is an entire line of code that produces an action")
print("")
print("iq/5 -> Expression")
print("it is a piece of code that produces a value")

print("\n Augmented assignement operator")
print("-----------------------\n")
some_value = 5
some_value += 2 
print(some_value)