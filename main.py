from typing import Any, List, Optional


class ZeroQuantityError(ValueError):
    """Пользовательское исключение для товаров с нулевым количеством."""

    def __init__(self, message: str = "Товар с нулевым количеством не может быть добавлен") -> None:
        self.message = message
        super().__init__(self.message)


class Product:

    def __init__(self, name: str, description: str, price: float, quantity: int) -> None:
        self.name = name
        self.description = description
        self.price = price

        if quantity == 0:
            raise ValueError("Товар с нулевым количеством не может быть добавлен")
        self.quantity = quantity


class Category:

    # Исправление ошибки 2: Используем Optional[List[Product]], так как дефолт равен None
    def __init__(self, name: str, description: str, products: Optional[List[Product]] = None) -> None:
        self.name = name
        self.description = description
        self.products = products if products is not None else []

    # Исправление ошибки 3: Добавлена аннотация возвращаемого типа -> None
    def add_product(self, product: Product) -> None:
        """Добавляет товар в категорию с полной обработкой исключений."""
        try:
            if product.quantity == 0:
                raise ZeroQuantityError()
        except ZeroQuantityError as e:
            print(f"Ошибка: {e}")
            raise
        else:
            self.products.append(product)
            print("Товар добавлен успешно")
        finally:
            print("Обработка добавления товара завершена")

    def middle_price(self) -> float:
        """Считает среднюю цену всех продуктов в категории."""
        try:
            total_price = sum(product.price for product in self.products)
            # Исправление ошибки 4: Приводим результат к float, чтобы mypy не ругался на Any
            return float(total_price / len(self.products))
        except ZeroDivisionError:
            return 0.0


if __name__ == "__main__":
    category_empty = Category("Пустая категория", "Категория без продуктов")
    print(f"Средняя цена в пустой категории: {category_empty.middle_price()}")

    product1 = Product("Samsung Galaxy S23", "Смартфон", 100000.0, 5)
    category1 = Category("Смартфоны", "Категория смартфонов")
    category1.add_product(product1)
    print(f"Средняя цена: {category1.middle_price()}\n")

    print("--- Попытка добавить некорректный товар ---")
    product_invalid = Product.__new__(Product)
    product_invalid.name = "Бракованный товар"
    product_invalid.price = 1000.0
    product_invalid.quantity = 0

    category1.add_product(product_invalid)
