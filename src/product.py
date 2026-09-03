from typing import Self


class Product:
    """Класс для описания товара в магазине."""

    name: str
    description: str
    price: float
    quantity: int

    def __init__(self, name: str, description: str, price: float, quantity: int):
        self.name = name
        self.description = description
        self.price = price
        self.quantity = quantity

    @classmethod
    def new_product(cls, product_data: dict, products_list: list["Product"] | None = None) -> Self:
        """Класс-метод принимает словарь с данными товара и возвращает созданный объект."""
        name = product_data.get("name", "")
        description = product_data.get("description", "")
        price = product_data.get("price", 0.0)
        quantity = product_data.get("quantity", 0)

        # Если передан список существующих товаров, ищем дубликат по имени
        if products_list:
            for existing_product in products_list:
                if existing_product.name == name:
                    # Складываем количество в наличии
                    existing_product.quantity += quantity
                    # Выбираем более высокую цену
                    existing_product.price = max(existing_product.price, price)
                    # Возвращаем обновленный существующий объект
                    return existing_product

        # Если дубликат не найден или список не передан, создаем новый объект класса
        return cls(name, description, price, quantity)
