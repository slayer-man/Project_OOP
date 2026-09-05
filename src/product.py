from typing import Any


class Product:
    """Класс для описания товара в магазине."""

    name: str
    description: str
    quantity: int

    def __init__(self, name: str, description: str, price: float, quantity: int):
        self.name = name
        self.description = description
        self.quantity = quantity
        if price <= 0:
            print("Цена не должна быть нулевая или отрицательная")
            self.__price = 0.0
        else:
            self.__price = price

    @classmethod
    def new_product(
        cls, product_data: dict, products_list: list["Product"] | None = None
    ) -> "Product":  # <--- ЗАМЕНИЛИ Self НА СТРОКУ "Product"
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
        return self.__price

    @price.setter
    def price(self, new_price: float) -> None:
        if new_price <= 0:
            print("Цена не должна быть нулевая или отрицательная")
            return

        if new_price < self.__price:
            user_answer = (
                input(f"Вы уверены, что хотите снизить цену с {self.__price} до {new_price} руб.? (y/n): ")
                .strip()
                .lower()
            )
            if user_answer != "y":
                print("Действие отменено. Цена осталась прежней.")
                return

        self.__price = new_price

    def __str__(self) -> str:
        return f"{self.name}, {self.price} руб. Остаток: {self.quantity} шт."

    def __add__(self, other: Any) -> float:
        if isinstance(other, Product):
            return (self.price * self.quantity) + (other.price * other.quantity)
        raise TypeError("Складывать можно только объекты класса Product")
