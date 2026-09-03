from src.product import Product


class Category:
    """Класс для описания категории товаров."""

    category_count = 0
    product_count = 0

    name: str
    description: str
    # Явно подсказываем mypy тип для приватной переменной на уровне класса (опционально)
    __products: list[Product]

    def __init__(self, name: str, description: str, products: list[Product] | None = None):
        self.name = name
        self.description = description
        # ДОБАВИЛИ АННОТАЦИЮ ТИПА ДЛЯ ПРИВАТНОГО СПИСКА
        self.__products: list[Product] = []

        Category.category_count += 1

        if products:
            for product in products:
                self.add_product(product)

    def add_product(self, product: Product) -> None:
        if isinstance(product, Product):
            self.__products.append(product)
            Category.product_count += 1
        else:
            raise TypeError("Добавить в категорию можно только объект класса Product")

    @property
    def products(self) -> str:
        product_strings = []
        for product in self.__products:
            product_strings.append(f"{product.name}, {product.price} руб. Остаток: {product.quantity} шт.")
        return "\n".join(product_strings)
