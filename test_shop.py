import pytest
from models import Product, Cart


@pytest.fixture
def product():
    return Product("book", 100, "This is a book", 1000)


@pytest.fixture
def cart():
    return Cart()


class TestProducts:

    def test_product_check_quantity(self, product):
        assert product.check_quantity(15) is True
        assert product.check_quantity(product.quantity) is True
        assert product.check_quantity(1001) is False

    def test_product_buy(self, product):
        product.buy(50)
        assert product.check_quantity(product.quantity)

    def test_product_buy_more_than_available(self, product):
        with pytest.raises(ValueError, match='Not enough items in the store'):
            product.buy(1100)
            assert ValueError('Not enough items in the store')


class TestCart:

    def test_add_product(self, cart, product):
        assert len(cart.products) == 0
        cart.add_product(product)
        assert len(cart.products) == 1
        assert cart.products[product] == 1

        cart.add_product(product, buy_count=2)
        assert cart.products[product] == 3

    def test_remove_product(self, cart, product):
        cart.add_product(product, buy_count=3)
        cart.remove_product(product, remove_count=1)
        assert cart.products[product] == 2

        cart.remove_product(product)
        assert product not in cart.products

    def test_clear_cart(self, cart, product):
        cart.add_product(product, buy_count=5)
        assert cart.products[product] == 5

        cart.clear()
        assert len(cart.products) == 0

    def test_get_total_price(self, cart, product):
        cart.add_product(product, buy_count=7)
        assert cart.products[product] == 7
        assert cart.get_total_price() == 700

    def test_buy(self, cart, product):
        cart.add_product(product, buy_count=101)
        assert cart.products[product] == 101

        cart.buy()

        assert product.check_quantity(product.quantity - 101)

    def test_buy_with_more_quantity(self, cart, product):
        cart.add_product(product, buy_count=1002)

        with pytest.raises(ValueError, match='Not enough products'):
            cart.buy()

        assert product.quantity == 1000
