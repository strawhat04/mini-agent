def parse(text):
    try:
        return int(text)
    except ValueError as e:
        raise RuntimeError(e)

try:
    parse("abc")
except RuntimeError as err:
    print(type(err.__cause__).__name__)    # ValueError
    print(type(err.__context__).__name__)  # ValueError (same object)