import importlib
from pkgutil import iter_modules

from tests import UnitTestResponse

bcolors = {
    'HEADER': '\033[95m',
    'OKBLUE': '\033[94m',
    'OKCYAN': '\033[96m',
    'OKGREEN': '\033[92m',
    'WARNING': '\033[93m',
    'FAIL': '\033[91m',
    'ENDC': '\033[0m',
    'BOLD': '\033[1m',
    'UNDERLINE': '\033[4m',
}

TESTS_DIR = 'tests'

def find_modules(path):
    modules = {}
    for _, name, ispkg in iter_modules([path]):
        if not ispkg:
            modules[name] = TESTS_DIR + '/' + name + '.py'
    return modules

test_modules = find_modules(TESTS_DIR)

print()

for module_name in test_modules:
    loader = importlib.machinery.SourceFileLoader(module_name, test_modules[module_name])
    module = loader.load_module(module_name)
    result = None
    message = ""
    try:
        result, message = module.Test.do()
    except Exception as e:
        print("Test " + module_name + f" {bcolors['FAIL']}FAILED WITH EXCEPTION{bcolors['ENDC']}")
        print(str(e), '\n')
        continue
    if result == UnitTestResponse.SUCCESS:
        print("Test " + module_name + f" {bcolors['OKGREEN']}PASSED{bcolors['ENDC']}")
    elif result == UnitTestResponse.ERROR:
        print("Test " + module_name + f" {bcolors['FAIL']}FAILED WITH MESSAGE{bcolors['ENDC']}")
        print(message)
    elif result == UnitTestResponse.WARNING:
        print("Test " + module_name + f" {bcolors['WARNING']}PASSED WITH WARNING{bcolors['ENDC']}")
        print(message)
    else:
        print("Test " + module_name + f" {bcolors['FAIL']}UNDEFINED STATUS CODE{bcolors['ENDC']}")
    print()
