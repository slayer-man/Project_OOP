import pytest
from src.category import Category, Order
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


def test_print_mixin_logs(capsys):
    """Проверяет, что PrintMixin выводит лог в консоль при создании объекта (Задание 2)."""
    _ = Product("Тест Миксина", "Описание", 100.0, 5)

    captured = capsys.readouterr()
    assert "Product('Тест Миксина', 'Описание', 100.0, 5)" in captured.out


def test_smartphone_initialization(sample_smartphone_1):
    """Проверяет корректность инициализации и уникальных свойств смартфона."""
    assert sample_smartphone_1.name == "Samsung Galaxy S23 Ultra"
    assert sample_smartphone_1.efficiency == 95.5
    assert sample_smartphone_1.model == "S23 Ultra"
    assert sample_smartphone_1.memory == 256
    assert sample_smartphone_1.color == "Серый"


def test_grass_initialization(sample_grass_1):
    """Проверяет корректность инициализации и уникальных свойств травы."""
    assert sample_grass_1.name == "Газонная трава"
    assert sample_grass_1.country == "Россия"
    assert sample_grass_1.germination_period == "7 дней"
    assert sample_grass_1.color == "Зеленый"


def test_strict_add_same_class(sample_smartphone_1, sample_smartphone_2):
    """Проверяет сложение продуктов одного и того же класса."""
    assert sample_smartphone_1 + sample_smartphone_2 == 2580000.0


def test_strict_add_different_classes(sample_smartphone_1, sample_grass_1):
    """Проверяет, что сложение продуктов РАЗНЫХ классов вызывает TypeError."""
    with pytest.raises(TypeError):
        _ = sample_smartphone_1 + sample_grass_1


def test_add_product_inheritance(sample_smartphone_1, sample_grass_1):
    """Проверяет, что категория принимает наследников Product."""
    category = Category("Смартфоны", "Гаджеты")
    category.add_product(sample_smartphone_1)
    category.add_product(sample_grass_1)

    assert Category.product_count == 2


def test_add_product_invalid_type():
    """Проверяет, что добавление объекта не-Product вызывает TypeError."""
    category = Category("Тест", "Описание")
    with pytest.raises(TypeError):
        category.add_product("Not a product")


def test_product_str(sample_smartphone_1):
    """Проверяет магический метод __str__ для продуктов."""
    assert str(sample_smartphone_1) == "Samsung Galaxy S23 Ultra, 180000.0 руб. Остаток: 5 шт."


def test_category_str(sample_smartphone_1, sample_smartphone_2):
    """Проверяет магический метод __str__ для категорий."""
    category = Category("Смартфоны", "Гаджеты", [sample_smartphone_1, sample_smartphone_2])
    assert str(category) == "Смартфоны, количество продуктов: 13 шт."


def test_product_iterator(sample_smartphone_1, sample_smartphone_2):
    """Проверяет корректность работы класса-итератора ProductIterator."""
    category = Category("Электроника", "Гаджеты", [sample_smartphone_1, sample_smartphone_2])
    iterator = ProductIterator(category)
    iterated_products = [product for product in iterator]
    assert len(iterated_products) == 2


def test_product_init_invalid_price(capsys):
    """Проверяет реакцию конструктора на некорректную цену."""
    product = Product("Брак", "Тест", -100.0, 5)
    assert product.price == 0.0

    captured = capsys.readouterr()
    assert "Цена не должна быть нулевая или отрицательная" in captured.out


def test_new_product_classmethod_merge_existing():
    """Проверяет слияние с существующим дубликатом в списке."""
    existing_product = Product("Дубликат", "Старый", 500.0, 2)
    products_list = [existing_product]

    data = {"name": "Дубликат", "description": "Новый", "price": 600.0, "quantity": 3}
    updated_product = Product.new_product(data, products_list)

    assert updated_product.quantity == 5
    assert updated_product.price == 600.0


def test_price_setter_invalid_value(capsys):
    """Проверяет запрет на установку отрицательной цены через сеттер."""
    product = Product("Товар", "Описание", 100.0, 5)
    product.price = -50.0
    assert product.price == 100.0

    captured = capsys.readouterr()
    assert "Цена не должна быть нулевая или отрицательная" in captured.out


def test_price_setter_decrease_confirmed(monkeypatch):
    """Проверяет успешное снижение цены при подтверждении 'y'."""
    product = Product("Товар", "Описание", 100.0, 5)
    monkeypatch.setattr("builtins.input", lambda _: "y")
    product.price = 80.0
    assert product.price == 80.0


def test_price_setter_decrease_cancelled(monkeypatch):
    """Проверяет отмену снижения цены при вводе 'n'."""
    product = Product("Товар", "Описание", 100.0, 5)
    monkeypatch.setattr("builtins.input", lambda _: "n")
    product.price = 80.0
    assert product.price == 100.0


def test_order_initialization():
    """Проверяет корректность инициализации и подсчета стоимости заказа (Задание 3)."""
    product = Product("Ноутбук", "Геймерский", 50000.0, 10)
    order = Order(product, 2)

    assert order.product.name == "Ноутбук"
    assert order.quantity_to_buy == 2
    assert order.total_price == 100000.0
    assert str(order) == "Заказ: Ноутбук, количество: 2 шт., Итого: 100000.0 руб."


def test_order_invalid_type():
    """Проверяет защиту конструктора Заказа от некорректных типов данных."""
    with pytest.raises(TypeError):
        _ = Order("Not a product", 5)  # type: ignore


def test_order_add_product_disabled():
    """Проверяет запрет на добавление других товаров в уже оформленный заказ."""
    product = Product("Ноутбук", "Геймерский", 50000.0, 10)
    order = Order(product, 2)
    with pytest.raises(NotImplementedError):
        order.add_product(product)


def test_base_product_cannot_be_instantiated():
    """Проверяет, что нельзя создать экземпляр абстрактного класса BaseProduct."""
    from src.product import BaseProduct

    with pytest.raises(TypeError):
        _ = BaseProduct()  # type: ignore
