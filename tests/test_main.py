import pytest
import runpy
from main import Product, Category, ZeroQuantityError


def test_product_creation_zero_quantity():
    """Тест Задания 1: Инициализация товара с 0 количеством вызывает ValueError."""
    with pytest.raises(ValueError) as exc_info:
        Product("Бракованный товар", "Описание", 1000.0, 0)
    assert str(exc_info.value) == "Товар с нулевым количеством не может быть добавлен"


def test_category_middle_price_zero_division():
    """Тест Задания 2: Пустая категория возвращает 0 через try/except."""
    category = Category("Пустая категория", "Описание")
    assert category.middle_price() == 0


def test_category_middle_price_success():
    """Тест Задания 2: Корректный подсчет средней цены."""
    p1 = Product("Товар 1", "Описание 1", 100.0, 2)
    p2 = Product("Товар 2", "Описание 2", 200.0, 3)
    category = Category("Категория", "Описание", [p1, p2])
    assert category.middle_price() == 150.0


def test_add_product_success(capsys):
    """Тест доп.

    задания: Успешное добавление товара (блок else и finally).
    """
    category = Category("Электроника", "Описание")
    product = Product("Ноутбук", "Описание", 50000.0, 1)

    category.add_product(product)

    captured = capsys.readouterr()
    assert "Товар добавлен успешно" in captured.out
    assert "Обработка добавления товара завершена" in captured.out
    assert len(category.products) == 1


def test_add_product_zero_quantity_error(capsys):
    """Тест доп.

    задания: Вызов исключения при добавлении товара с количеством 0.
    """
    category = Category("Электроника", "Описание")

    # Создаем объект в обход __init__, чтобы проверить именно метод add_product
    product_invalid = Product.__new__(Product)
    product_invalid.quantity = 0

    with pytest.raises(ZeroQuantityError):
        category.add_product(product_invalid)

    captured = capsys.readouterr()
    assert "Ошибка: Товар с нулевым количеством не может быть добавлен" in captured.out
    assert "Обработка добавления товара завершена" in captured.out


def test_main_execution():
    """Тестирует выполнение демонстрационного блока if __name__ == '__main__'."""
    # Перехватываем базовое исключение Exception, так как имя класса внутри runpy меняется на __main__
    with pytest.raises(Exception) as exc_info:
        runpy.run_path("main.py", run_name="__main__")

    # Проверяем, что упало именно с нужным нам текстом ошибки
    assert "Товар с нулевым количеством не может быть добавлен" in str(exc_info.value)

