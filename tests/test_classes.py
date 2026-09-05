import pytest
from src.category import Category
from src.product import Product, Smartphone, LawnGrass
from src.utils import ProductIterator


@pytest.fixture(autouse=True)
def reset_category_counters():
    """Фикстура автоматически обнуляет счетчики класса перед каждым тестом."""
    Category.category_count = 0
    Category.product_count = 0


@pytest.fixture
def sample_smartphone_1():
    """Тестовый смартфон 1."""
    return Smartphone(
        "Samsung Galaxy S23 Ultra", "256GB, Серый цвет", 180000.0, 5, 95.5, "S23 Ultra", 256, "Серый"
    )


@pytest.fixture
def sample_smartphone_2():
    """Тестовый смартфон 2."""
    return Smartphone(
        "Iphone 15", "512GB, Gray space", 210000.0, 8, 98.2, "15", 512, "Gray space"
    )


@pytest.fixture
def sample_grass_1():
    """Тестовая трава 1."""
    return LawnGrass(
        "Газонная трава", "Элитная трава для газона", 500.0, 20, "Россия", "7 дней", "Зеленый"
    )


def test_smartphone_initialization(sample_smartphone_1):
    """Проверяет корректность инициализации и уникальных свойств смартфона (Задание 4)."""
    assert sample_smartphone_1.name == "Samsung Galaxy S23 Ultra"
    assert sample_smartphone_1.efficiency == 95.5
    assert sample_smartphone_1.model == "S23 Ultra"
    assert sample_smartphone_1.memory == 256
    assert sample_smartphone_1.color == "Серый"


def test_grass_initialization(sample_grass_1):
    """Проверяет корректность инициализации и уникальных свойств травы (Задание 4)."""
    assert sample_grass_1.name == "Газонная трава"
    assert sample_grass_1.country == "Россия"
    assert sample_grass_1.germination_period == "7 дней"
    assert sample_grass_1.color == "Зеленый"


def test_strict_add_same_class(sample_smartphone_1, sample_smartphone_2):
    """Проверяет сложение продуктов одного и того же класса (Задание 4)."""
    assert sample_smartphone_1 + sample_smartphone_2 == 2580000.0


def test_strict_add_different_classes(sample_smartphone_1, sample_grass_1):
    """Проверяет, что сложение продуктов РАЗНЫХ классов вызывает TypeError (Задание 4)."""
    with pytest.raises(TypeError):
        _ = sample_smartphone_1 + sample_grass_1


def test_add_product_inheritance(sample_smartphone_1, sample_grass_1):
    """Проверяет, что категория принимает наследников Product (Задание 4)."""
    category = Category("Смартфоны", "Гаджеты")
    category.add_product(sample_smartphone_1)
    category.add_product(sample_grass_1)

    assert Category.product_count == 2


def test_add_product_invalid_type():
    """Проверяет, что добавление объекта не-Product вызывает TypeError (Задание 4)."""
    category = Category("Тест", "Описание")
    with pytest.raises(TypeError):
        category.add_product("Not a product")


def test_product_str(sample_smartphone_1):
    assert str(sample_smartphone_1) == "Samsung Galaxy S23 Ultra, 180000.0 руб. Остаток: 5 шт."


def test_category_str(sample_smartphone_1, sample_smartphone_2):
    category = Category(
        "Смартфоны", "Гаджеты", [sample_smartphone_1, sample_smartphone_2]
    )
    assert str(category) == "Смартфоны, количество продуктов: 13 шт."


def test_product_iterator(sample_smartphone_1, sample_smartphone_2):
    category = Category("Электроника", "Гаджеты", [sample_smartphone_1, sample_smartphone_2])
    iterator = ProductIterator(category)
    iterated_products = [product for product in iterator]
    assert len(iterated_products) == 2


def test_product_init_invalid_price(capsys):
    """Проверяет реакцию конструктора на некорректную цену (строки 16-17)."""
    product = Product("Брак", "Тест", -100.0, 5)
    assert product.price == 0.0

    # Проверяем, что в консоль вывелось предупреждение
    captured = capsys.readouterr()
    assert "Цена не должна быть нулевая или отрицательная" in captured.out


def test_new_product_classmethod_new():
    """Проверяет создание абсолютно нового продукта через класс-метод (строки 26-38)."""
    data = {"name": "Новинка", "description": "Свежий товар", "price": 1000.0, "quantity": 10}
    product = Product.new_product(data)
    assert product.name == "Новинка"
    assert product.price == 1000.0


def test_new_product_classmethod_merge_existing():
    """Проверяет слияние с существующим дубликатом в списке (строки 26-38)."""
    existing_product = Product("Дубликат", "Старый", 500.0, 2)
    products_list = [existing_product]

    data = {"name": "Дубликат", "description": "Новый", "price": 600.0, "quantity": 3}
    updated_product = Product.new_product(data, products_list)

    # Количество должно сложиться: 2 + 3 = 5
    assert updated_product.quantity == 5
    # Цена должна стать максимальной: 600.0
    assert updated_product.price == 600.0
    assert updated_product is existing_product


def test_price_setter_invalid_value(capsys):
    """Проверяет запрет на установку отрицательной цены через сеттер (строки 48-64)."""
    product = Product("Товар", "Описание", 100.0, 5)
    product.price = -50.0
    assert product.price == 100.0

    captured = capsys.readouterr()
    assert "Цена не должна быть нулевая или отрицательная" in captured.out


def test_price_setter_decrease_confirmed(monkeypatch):
    """Проверяет успешное снижение цены при подтверждении 'y' (строки 48-64)."""
    product = Product("Товар", "Описание", 100.0, 5)

    # Имитируем ввод пользователя 'y'
    monkeypatch.setattr("builtins.input", lambda _: "y")
    product.price = 80.0
    assert product.price == 80.0


def test_price_setter_decrease_cancelled(monkeypatch):
    """Проверяет отмену снижения цены при вводе 'n' (строки 48-64)."""
    product = Product("Товар", "Описание", 100.0, 5)

    # Имитируем ввод пользователя 'n'
    monkeypatch.setattr("builtins.input", lambda _: "n")
    product.price = 80.0
    assert product.price == 100.0  # Цена не изменилась
