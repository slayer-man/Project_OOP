from src.product import Product


class Category:
    """Класс для описания категории товаров."""

    # Атрибуты класса для хранения общей статистики
    category_count = 0
    product_count = 0

    name: str
    description: str
    __products: list[Product]

    def __init__(
        self, name: str, description: str, products: list[Product] | None = None
    ):
        self.name = name
        self.description = description
        self.__products = []

        # Автоматически увеличиваем счетчик категорий при создании
        Category.category_count += 1

        # Если при инициализации передали список товаров, добавляем их через метод
        if products:
            for product in products:
                self.add_product(product)

    def add_product(self, product: Product) -> None:
        """Метод для добавления объекта Product или его наследников в приватный список товаров (Задание 3)."""
        if isinstance(product, Product) and issubclass(type(product), Product):
            self.__products.append(product)
            # При добавлении каждого уникального товара увеличиваем счетчик
            Category.product_count += 1
        else:
            raise TypeError(
                "Добавить в категорию можно только объект класса Product или его наследников"
            )

    @property
    def products(self) -> str:
        """Оптимизированный геттер: преобразует объекты продуктов в строки через str()."""
        product_strings = []
        for product in self.__products:
            product_strings.append(str(product))
        return "\n".join(product_strings)

    def __str__(self) -> str:
        """Возвращает строковое представление категории с подсчетом всех штук на складе."""
        total_quantity = sum(product.quantity for product in self.__products)
        return f"{self.name}, количество продуктов: {total_quantity} шт."
