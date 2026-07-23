import src.slotmachine as sm

def test_checking_win():
    assert sm._is_win(1) # bar bar bar 
    assert not sm._is_win(2)
