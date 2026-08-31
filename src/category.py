from src.product import Product


class Category:
    """Класс для описания категории товаров."""

    # Атрибуты класса для хранения общей статистики
    category_count = 0
    product_count = 0

    name: str
    description: str
    products: list[Product]

    def __init__(self, name: str, description: str, products: list[Product]):
        self.name = name
        self.description = description
        self.products = products

        # Автоматически увеличиваем счетчики при создании новой категории
        Category.category_count += 1
        Category.product_count += len(products)
