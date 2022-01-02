def gen_type_check(gen_fn):
    a = gen_fn(True)
    b = gen_fn(False)
    
    return type(a) == float and type(b) == str

def gen_range_check(gen_fn):
    for i in range(100):
        a = gen_fn(True)

        if a < 0 or a > 1:
            return False

    for i in range(100):
        b = gen_fn(False)

        if b not in ['A','B','C']:
            return False

    return True

def len_output_check(gen):
    a = [len(gen(n)) == n for n in [5,10,50]]
    return all(a)

def failing_test(f):
    return False