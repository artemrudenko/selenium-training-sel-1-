import pytest
from .data_providers import valid_products


@pytest.mark.parametrize("products", valid_products, ids=[repr(x) for x in valid_products])
def test_cart_workflow(app, products):
    old_size = app.get_current_cart_size()
    diff = 0
    expected = []
    for p in products:
        expected.append(p.name)
        app.add_product_to_cart(p)
        diff += p.amount
    new_size = app.get_current_cart_size()
    assert new_size == old_size + diff
    assert sorted(app.get_products_in_cart()) == sorted(expected)
    app.clear_cart()
    assert app.get_products_in_cart() == []
    assert app.get_current_cart_size() == 0

