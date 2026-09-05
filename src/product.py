from typing import Any, Self


class Product:
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

    @classmethod
    def new_product(
        cls, product_data: dict, products_list: list["Product"] | None = None
    ) -> Self:
        """Класс-метод принимает словарь с данными товара и возвращает созданный объект."""
        name = product_data.get("name", "")
        description = product_data.get("description", "")
        price = product_data.get("price", 0.0)
        quantity = product_data.get("quantity", 0)

        if products_list:
            for existing_product in products_list:
                if existing_product.name == name:
                    existing_product.quantity += quantity
                    # Используем сеттер для изменения цены (сработает логика проверки)
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

        # Если цена снижается, запрашиваем подтверждение пользователя
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

        # Устанавливаем новую цену, если все проверки пройдены
        self.__price = new_price

    def __str__(self) -> str:
        """Возвращает строковое представление продукта."""
        return f"{self.name}, {self.price} руб. Остаток: {self.quantity} шт."

    def __add__(self, other: Any) -> float:
        """Складывает полную стоимость остатков двух товаров строго одного и того же класса (Задание 2)."""
        if type(self) is type(other):
            return (self.price * self.quantity) + (other.price * other.quantity)
        raise TypeError("Складывать можно только продукты одного и того же класса")


class Smartphone(Product):
    """Дочерний класс для описания смартфонов (Задание 1)."""

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
        super().__init__(name, description, price, quantity)
        self.efficiency = efficiency
        self.model = model
        self.memory = memory
        self.color = color


class LawnGrass(Product):
    """Дочерний класс для описания газонной травы (Задание 1)."""

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
        super().__init__(name, description, price, quantity)
        self.country = country
        self.germination_period = germination_period
        self.color = color
