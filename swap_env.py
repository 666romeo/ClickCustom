mode = str(input('Выбери режим разработки portable/remote: '))

if mode == 'portable':
    with open('app/settings.py', 'r') as f:
        old_data = f.read()
    try:
        new_data = old_data.replace("MODE = 'remote'", "MODE = 'portable'")
        with open('app/settings.py', 'w') as f:
            f.write(new_data)
    except:
        pass

if mode == 'remote':
    with open('app/settings.py', 'r') as f:
        old_data = f.read()
    try:
        new_data = old_data.replace("MODE = 'portable'", "MODE = 'remote'")
        with open('app/settings.py', 'w') as f:
            f.write(new_data)
    except:
        pass