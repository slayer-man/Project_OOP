from src.product import Product


class Category:
    """Класс для описания категории товаров."""

    # Атрибуты класса для хранения общей статистики
    category_count = 0
    product_count = 0

    name: str
    description: str

    def __init__(
        self, name: str, description: str, products: list[Product] | None = None
    ):
        self.name = name
        self.description = description
        # Делаем список товаров приватным атрибутом
        self.__products = []

        # Автоматически увеличиваем счетчик категорий при создании
        Category.category_count += 1

        # Если при инициализации передали список товаров, добавляем их через метод
        if products:
            for product in products:
                self.add_product(product)

    def add_product(self, product: Product) -> None:
        """Метод для добавления объекта Product в приватный список товаров."""
        if isinstance(product, Product):
            self.__products.append(product)
            # При добавлении каждого уникального товара увеличиваем счетчик
            Category.product_count += 1
        else:
            raise TypeError("Добавить в категорию можно только объект класса Product")

    @property
    def products(self) -> str:
        """Геттер возвращает список товаров в виде отформатированных строк."""
        product_strings = []
        for product in self.__products:
            product_strings.append(
                f"{product.name}, {product.price} руб. Остаток: {product.quantity} шт."
            )
        return "\n".join(product_strings)
