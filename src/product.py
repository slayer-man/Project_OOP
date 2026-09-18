from abc import ABC, abstractmethod
from typing import Any


class BaseProduct(ABC):
    """Абстрактный базовый класс для всех продуктов."""

    @abstractmethod
    def __str__(self) -> str:
        pass

    @abstractmethod
    def __add__(self, other: Any) -> float:
        pass


class PrintMixin:
    """Класс-миксин для логирования создания объекта в консоль."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        # Выводим текстовое представление объекта в консоль в момент его создания
        print(repr(self))


class Product(PrintMixin, BaseProduct):
    """Базовый класс для описания товара в магазине."""

    name: str
    description: str
    quantity: int

    def __init__(self, name: str, description: str, price: float, quantity: int):
        self.name = name
        self.description = description
        self.quantity = quantity

        # Делаем атрибут цены приватным при инициализации
        if price <= 0:
            print("Цена не должна быть нулевая или отрицательная")
            self.__price = 0.0
        else:
            self.__price = price

        # Вызов конструктора миксина для печати лога
        super().__init__()

    @classmethod
    def new_product(
            cls, product_data: dict, products_list: list["Product"] | None = None
    ) -> "Product":
        """Класс-метод принимает словарь с данными товара и возвращает созданный объект."""
        name = product_data.get("name", "")
        description = product_data.get("description", "")
        price = product_data.get("price", 0.0)
        quantity = product_data.get("quantity", 0)

        if products_list:
            for existing_product in products_list:
                if existing_product.name == name:
                    existing_product.quantity += quantity
                    existing_product.price = max(existing_product.price, price)
                    return existing_product

        return cls(name, description, price, quantity)

    @property
    def price(self) -> float:
        """Геттер для получения приватного атрибута цены."""
        return self.__price

    @price.setter
    def price(self, new_price: float) -> None:
        """Сеттер для изменения цены с проверками и подтверждением снижения."""
        if new_price <= 0:
            print("Цена не должна быть нулевая или отрицательная")
            return

        if new_price < self.__price:
            user_answer = (
                input(
                    f"Вы уверены, что хотите снизить цену с {self.__price} до {new_price} руб.? (y/n): "
                )
                .strip()
                .lower()
            )
            if user_answer != "y":
                print("Действие отменено. Цена осталась прежней.")
                return

        self.__price = new_price

    def __str__(self) -> str:
        """Возвращает строковое представление продукта."""
        return f"{self.name}, {self.price} руб. Остаток: {self.quantity} шт."

    def __add__(self, other: Any) -> float:
        """Складывает полную стоимость остатков двух товаров строго одного и того же класса."""
        if type(self) is type(other):
            return (self.price * self.quantity) + (other.price * other.quantity)
        raise TypeError("Складывать можно только продукты одного и того же класса")

    def __repr__(self) -> str:
        """Возвращает строковое представление для логирования."""
        return f"{self.__class__.__name__}('{self.name}', '{self.description}', {self.price}, {self.quantity})"


class Smartphone(Product):
    """Дочерний класс для описания смартфонов."""

    def __init__(
            self,
            name: str,
            description: str,
            price: float,
            quantity: int,
            efficiency: float,
            model: str,
            memory: int,
            color: str,
    ):
        self.efficiency = efficiency
        self.model = model
        self.memory = memory
        self.color = color
        super().__init__(name, description, price, quantity)


class LawnGrass(Product):
    """Дочерний класс для описания газонной травы."""

    def __init__(
            self,
            name: str,
            description: str,
            price: float,
            quantity: int,
            country: str,
            germination_period: str,
            color: str,
    ):
        self.country = country
        self.germination_period = germination_period
        self.color = color
        super().__init__(name, description, price, quantity)
