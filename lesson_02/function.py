def foo(arg1, *args, **kwargs):
    pass


# contact_info = "john,smith,nyst 12 av,+380991112233,male"
# name, *_, phone, sex = contact_info.split(',')

# print(name)
# print(phone)
# print(sex)

# info, info2 =['john', 'smith', 'nyst 12 av', '+380991112233', 'male'] # -> ValueError: too many values to unpack (expected 2)
# name, surname, address, phone, sex  =['john', 'smith', 'nyst 12 av', '+380991112233', 'male']

name, surname, *args = ['john', 'smith', 'nyst 12 av', '+380991112233', 'male']

print(name)  # -> john
print(surname)  # -> smith
print(args)  # -> ['nyst 12 av', '+380991112233', 'male']
