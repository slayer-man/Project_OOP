from abc import ABC, abstractmethod
from src.product import Product


class BaseGroup(ABC):
    """Абстрактный базовый класс для групп товаров (Доп. задание к Заданию 3)."""

    @abstractmethod
    def __init__(self, name: str, description: str) -> None:
        pass

    @abstractmethod
    def add_product(self, product: Product) -> None:
        pass

    @abstractmethod
    def __str__(self) -> str:
        pass


class Category(BaseGroup):
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
        """Метод для добавления объекта Product или его наследников в приватный список товаров."""
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


class Order(BaseGroup):
    """Класс для описания заказа на покупку одного товара (Доп. задание к Заданию 3)."""

    def __init__(self, product: Product, quantity_to_buy: int):
        if not isinstance(product, Product):
            raise TypeError(
                "В заказе можно указать только продукт класса Product или его наследников"
            )

        self.product = product
        self.quantity_to_buy = quantity_to_buy
        self.name = f"Заказ на {product.name}"
        self.description = f"Покупка товара {product.name} в количестве {quantity_to_buy} шт."
        # Итоговая стоимость рассчитывается автоматически при создании
        self.total_price = product.price * quantity_to_buy

    def add_product(self, product: Product) -> None:
        """Заказ оформляется на один конкретный товар. Добавление других запрещено."""
        raise NotImplementedError(
            "Нельзя добавлять другие товары в уже оформленный заказ"
        )

    def __str__(self) -> str:
        return f"Заказ: {self.product.name}, количество: {self.quantity_to_buy} шт., Итого: {self.total_price} руб."
