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


@pytest.fixture
def sample_category(sample_product):
    """Фикстура для создания тестовой категории с одним продуктом."""
    return Category("Электроника", "Гаджеты", [sample_product])


def test_product_initialization(sample_product):
    """Тест проверяет корректность инициализации объекта Product."""
    assert sample_product.name == "Samsung Galaxy S23"
    assert sample_product.description == "Смартфон"
    assert sample_product.price == 80000.0
    assert sample_product.quantity == 5


def test_category_initialization(sample_category, sample_product):
    """Тест проверяет корректность инициализации объекта Category."""
    assert sample_category.name == "Электроника"
    assert sample_category.description == "Гаджеты"
    assert sample_category.products == [sample_product]


def test_category_and_product_counters(sample_product):
    """Тест проверяет корректность подсчета категорий и уникальных продуктов."""
    # До создания объектов счетчики должны быть 0 благодаря фикстуре сброса
    assert Category.category_count == 0
    assert Category.product_count == 0

    # Создаем первую категорию с 1 товаром
    Category("Электроника", "Гаджеты", [sample_product])
    assert Category.category_count == 1
    assert Category.product_count == 1

    # Создаем вторую категорию с 2 товарами
    prod2 = Product("iPhone 15", "Смартфон", 90000.0, 3)
    prod3 = Product("Xiaomi 13", "Смартфон", 40000.0, 10)
    Category("Телефоны", "Мобильные", [prod2, prod3])

    # Проверяем общие счетчики на уровне класса
    assert Category.category_count == 2
    assert Category.product_count == 3
