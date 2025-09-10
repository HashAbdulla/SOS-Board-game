import prime_utils

def test_prime_number():
    assert prime_utils.is_prime(7) == True  # 7 is prime

def test_non_prime_number():
    assert prime_utils.is_prime(8) == False  # 8 is not prime

def test_edge_case_zero():
    assert prime_utils.is_prime(0) == False  # 0 is not prime

def test_edge_case_one():
    assert prime_utils.is_prime(1) == False  # 1 is not prime