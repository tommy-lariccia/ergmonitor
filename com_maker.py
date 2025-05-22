import json

fdata = dict()
fdata['commands'] = dict()

while True:
    if input('Are there any more commands? ') != 'y':
        break
    com_name = input("What is the command name? ")
    com_id = input("What is the command identifier? ")
    cargs = []
    rargs = []
    while True:
        if input('Are there any more command args? ') != 'y':
            break
        arg = dict()
        arg["name"] = input('What is the arg name? ')
        arg["type"] = input('What is the arg type? ')
        arg["bcount"] = int(input('How many bytes does the arg have? '))
        arg["endianness"] = input('What is the arg\'s endianness? (big / little) ')
        cargs.append(arg)
    while True:
        if input('Are there any more response args? ') != 'y':
            break
        arg = dict()
        arg["name"] = input('What is the arg name? ')
        arg["type"] = input('What is the arg type? ')
        arg["bcount"] = int(input('How many bytes does the arg have? '))
        arg["endianness"] = input('What is the arg\'s endianness? (big / little) ')
        rargs.append(arg)
    data = dict()
    data["name"] = com_name
    data["com_id"] = com_id
    data["cargs"] = cargs
    data["rargs"] = rargs
    fdata['commands'][com_name] = data

print(json.dumps(fdata))
