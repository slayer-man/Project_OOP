import pytest
from src.category import Category
from src.product import Product


@pytest.fixture(autouse=True)
def reset_category_counters():
    """Фикстура автоматически обнуляет счетчики класса перед каждым тестом."""
    Category.category_count = 0
    Category.product_count = 0


@pytest.fixture
def sample_product():
    """Фикстура для создания тестового продукта."""
    return Product("Samsung Galaxy S23", "Смартфон", 80000.0, 5)


def test_category_private_products_and_getter(sample_product):
    """Проверяет приватность списка товаров и работу строкового геттера."""
    category = Category("Электроника", "Гаджеты", [sample_product])

    with pytest.raises(AttributeError):
        category.__products

    expected_output = "Samsung Galaxy S23, 80000.0 руб. Остаток: 5 шт."
    assert category.products == expected_output


def test_new_product_classmethod():
    """Проверяет создание продукта через фабричный класс-метод."""
    data = {
        "name": "Xiaomi Redmi 13",
        "description": "Бюджетный смартфон",
        "price": 20000.0,
        "quantity": 10,
    }
    product = Product.new_product(data)

    assert product.name == "Xiaomi Redmi 13"
    assert product.price == 20000.0
    assert product.quantity == 10


def test_new_product_merge_duplicates():
    """Проверяет слияние дубликатов товаров по имени."""
    products_list = [Product("iPhone 15", "Базовый", 90000.0, 2)]
    new_data = {
        "name": "iPhone 15",
        "description": "Новый цвет",
        "price": 95000.0,
        "quantity": 3,
    }

    updated_product = Product.new_product(new_data, products_list)

    assert updated_product.quantity == 5
    assert updated_product.price == 95000.0


def test_price_setter_invalid():
    """Проверяет защиту сеттера от нулевой или отрицательной цены."""
    product = Product("Тест", "Описание", 100.0, 1)

    product.price = -50.0
    assert product.price == 100.0

    product.price = 0.0
    assert product.price == 100.0


def test_price_setter_decrease_confirmed(monkeypatch):
    """Проверяет успешное снижение цены при подтверждении 'y'."""
    product = Product("Тест", "Описание", 100.0, 1)
    monkeypatch.setattr("builtins.input", lambda _: "y")

    product.price = 80.0
    assert product.price == 80.0


def test_price_setter_decrease_cancelled(monkeypatch):
    """Проверяет отмену снижения цены при вводе 'n'."""
    product = Product("Тест", "Описание", 100.0, 1)
    monkeypatch.setattr("builtins.input", lambda _: "n")

    product.price = 80.0
    assert product.price == 100.0
