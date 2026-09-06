import pytest
from src.category import Category, Order
from src.product import Product, Smartphone, LawnGrass


@pytest.fixture(autouse=True)
def reset_category_counters():
    """Фикстура автоматически обнуляет счетчики класса перед каждым тестом."""
    Category.category_count = 0
    Category.product_count = 0


def test_print_mixin_logs(capsys):
    """Проверяет, что PrintMixin выводит лог в консоль при создании объекта."""
    _ = Product("Тест Миксина", "Описание", 100.0, 5)

    captured = capsys.readouterr()
    assert "Product('Тест Миксина', 'Описание', 100.0, 5)" in captured.out


def test_order_initialization():
    """Проверяет корректность инициализации и подсчета стоимости заказа."""
    product = Product("Ноутбук", "Геймерский", 50000.0, 10)
    order = Order(product, 2)

    assert order.product.name == "Ноутбук"
    assert order.quantity_to_buy == 2
    assert order.total_price == 100000.0
    assert (
        str(order)
        == "Заказ: Ноутбук, количество: 2 шт., Итого: 100000.0 руб."
    )


def test_order_invalid_type():
    """Проверяет защиту конструктора Заказа от некорректных типов данных."""
    with pytest.raises(TypeError):
        _ = Order("Not a product", 5)  # type: ignore


def test_base_product_cannot_be_instantiated():
    """Проверяет, что нельзя создать экземпляр абстрактного класса BaseProduct."""
    from src.product import BaseProduct

    with pytest.raises(TypeError):
        _ = BaseProduct()  # type: ignore
