import pytest
from order_processing_refactored import process_checkout

def test_ok_no_coupon():
    r = process_checkout({"user_id": 1, "items": [{"price": 50, "qty": 2}], "coupon": None, "currency": "USD"})
    assert r["subtotal"] == 100
    assert r["discount"] == 0
    assert r["tax"] == 21
    assert r["total"] == 121

def test_ok_save10():
    r = process_checkout({"user_id": 2, "items": [{"price": 30, "qty": 3}], "coupon": "SAVE10", "currency": "USD"})
    assert r["discount"] == 9

def test_ok_save20():
    r = process_checkout({"user_id": 3, "items": [{"price": 100, "qty": 2}], "coupon": "SAVE20", "currency": "USD"})
    assert r["discount"] == 40

def test_unknown_coupon():
    with pytest.raises(ValueError):
        process_checkout({"user_id": 1, "items": [{"price": 10, "qty": 1}], "coupon": "???", "currency": "USD"})

def test_validation_user_id():
    with pytest.raises(ValueError, match="user_id is required"):
        process_checkout({"items": [{"price": 10, "qty": 1}]})

def test_validation_items():
    with pytest.raises(ValueError, match="items is required"):
        process_checkout({"user_id": 1})

def test_validation_items_list():
    with pytest.raises(ValueError, match="items must be a list"):
        process_checkout({"user_id": 1, "items": "not a list"})

def test_validation_items_empty():
    with pytest.raises(ValueError, match="items must not be empty"):
        process_checkout({"user_id": 1, "items": []})

def test_validation_item_price_qty():
    with pytest.raises(ValueError, match="item must have price and qty"):
        process_checkout({"user_id": 1, "items": [{"price": 10}]})

def test_validation_price_positive():
    with pytest.raises(ValueError, match="price must be positive"):
        process_checkout({"user_id": 1, "items": [{"price": 0, "qty": 1}]})

def test_validation_qty_positive():
    with pytest.raises(ValueError, match="qty must be positive"):
        process_checkout({"user_id": 1, "items": [{"price": 10, "qty": 0}]})
