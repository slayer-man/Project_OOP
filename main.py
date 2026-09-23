class ZeroQuantityError(ValueError):
    """Пользовательское исключение для товаров с нулевым количеством."""

    def __init__(self, message="Товар с нулевым количеством не может быть добавлен"):
        self.message = message
        super().__init__(self.message)


class Product:

    def __init__(self, name: str, description: str, price: float, quantity: int):
        self.name = name
        self.description = description
        self.price = price

        # Выбрасываем базовое исключение, если количество равно 0
        if quantity == 0:
            raise ValueError("Товар с нулевым количеством не может быть добавлен")
        self.quantity = quantity


class Category:

    def __init__(self, name: str, description: str, products: list = None):
        self.name = name
        self.description = description
        self.products = products if products is not None else []

    def add_product(self, product: Product):
        """Добавляет товар в категорию с полной обработкой исключений """
        try:
            if product.quantity == 0:
                raise ZeroQuantityError()
        except ZeroQuantityError as e:
            print(f"Ошибка: {e}")
            raise  # Перевызываем, чтобы прервать программу.
        else:
            self.products.append(product)
            print("Товар добавлен успешно")
        finally:
            print("Обработка добавления товара завершена")

    def middle_price(self) -> float:
        """Считает среднюю цену всех продуктов в категории"""
        try:
            total_price = sum(product.price for product in self.products)
            return total_price / len(self.products)
        except ZeroDivisionError:
            return 0


if __name__ == "__main__":
    # 1. Проверяем расчет средней цены
    category_empty = Category("Пустая категория", "Категория без продуктов")
    print(f"Средняя цена в пустой категории: {category_empty.middle_price()}")

    # 2. Проверяем успешное добавление (блок else и finally)
    product1 = Product("Samsung Galaxy S23", "Смартфон", 100000.0, 5)
    category1 = Category("Смартфоны", "Категория смартфонов")
    category1.add_product(product1)
    print(f"Средняя цена: {category1.middle_price()}\n")

    # 3. Проверяем добавление некорректного товара (блок except и finally)
    print("--- Попытка добавить некорректный товар ---")
    # Создаем через обход __init__, чтобы протестировать именно метод add_product
    product_invalid = Product.__new__(Product)
    product_invalid.name = "Бракованный товар"
    product_invalid.price = 1000.0
    product_invalid.quantity = 0

    category1.add_product(product_invalid)
