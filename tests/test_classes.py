import pytest
from src.category import Category
from src.product import Product
from src.utils import ProductIterator


@pytest.fixture(autouse=True)
def reset_category_counters():
    """Фикстура автоматически обнуляет счетчики класса перед каждым тестом."""
    Category.category_count = 0
    Category.product_count = 0


@pytest.fixture
def sample_product_1():
    """Первый тестовый продукт."""
    return Product("Samsung Galaxy S23", "Смартфон", 80000.0, 5)


@pytest.fixture
def sample_product_2():
    """Второй тестовый продукт."""
    return Product("iPhone 15", "Смартфон", 100000.0, 3)


def test_product_str(sample_product_1):
    """Проверяет магический метод __str__ для класса Product."""
    assert str(sample_product_1) == "Samsung Galaxy S23, 80000.0 руб. Остаток: 5 шт."


def test_category_str(sample_product_1, sample_product_2):
    """Проверяет магический метод __str__ для класса Category."""
    category = Category("Электроника", "Гаджеты", [sample_product_1, sample_product_2])
    assert str(category) == "Электроника, количество продуктов: 8 шт."


def test_product_add(sample_product_1, sample_product_2):
    """Проверяет магический метод сложения __add__ для двух продуктов."""
    result = sample_product_1 + sample_product_2
    assert result == 700000.0


def test_product_add_type_error(sample_product_1):
    """Проверяет, что сложение продукта с объектом другого типа вызывает TypeError."""
    with pytest.raises(TypeError):
        sample_product_1 + 100


def test_product_iterator(sample_product_1, sample_product_2):
    """Проверяет корректность работы класса-итератора ProductIterator."""
    category = Category("Электроника", "Гаджеты", [sample_product_1, sample_product_2])
    iterator = ProductIterator(category)

    iterated_products = [product for product in iterator]

    assert len(iterated_products) == 2
    assert iterated_products[0] == sample_product_1
    assert iterated_products[1] == sample_product_2


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


def test_price_setter_invalid():
    """Проверяет защиту сеттера от нулевой или отрицательной цены."""
    product = Product("Тест", "Описание", 100.0, 1)

    product.price = -50.0
    assert product.price == 100.0  # Цена не изменилась

    product.price = 0.0
    assert product.price == 100.0  # Цена не изменилась


def test_price_setter_decrease_confirmed(monkeypatch):
    """Проверяет успешное снижение цены при подтверждении 'y'."""
    product = Product("Тест", "Описание", 100.0, 1)

    # Имитируем ввод пользователя 'y' в консоль
    monkeypatch.setattr("builtins.input", lambda _: "y")

    product.price = 80.0
    assert product.price == 80.0


def test_price_setter_decrease_cancelled(monkeypatch):
    """Проверяет отмену снижения цены при вводе 'n'."""
    product = Product("Тест", "Описание", 100.0, 1)

    # Имитируем ввод пользователя 'n' в консоль
    monkeypatch.setattr("builtins.input", lambda _: "n")

    product.price = 80.0
    assert product.price == 100.0  # Цена осталась прежней
