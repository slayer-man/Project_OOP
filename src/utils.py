import json
import os
from typing import Any

from src.category import Category
from src.product import Product


def load_data_from_json(file_path: str) -> list[Category]:
    """Читает JSON-файл и возвращает список объектов класса Category."""
    if not os.path.exists(file_path):
        return []

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
    except json.JSONDecodeError:
        return []

    categories = []
    for category_data in data:
        products = []
        for product_data in category_data.get("products", []):
            product = Product(
                name=product_data["name"],
                description=product_data["description"],
                price=product_data["price"],
                quantity=product_data["quantity"],
            )
            products.append(product)

        category = Category(
            name=category_data["name"],
            description=category_data["description"],
            products=products,
        )
        categories.append(category)

    return categories


class ProductIterator:
    """Вспомогательный класс для перебора товаров категории в цикле for (Доп. задание)."""

    def __init__(self, category: Category):
        self.products: list[Product] = getattr(category, "_Category__products")
        self.index = 0

    def __iter__(self) -> "ProductIterator":
        return self

    def __next__(self) -> Any:
        if self.index < len(self.products):
            product = self.products[self.index]
            self.index += 1
            return product
        else:
            raise StopIteration
