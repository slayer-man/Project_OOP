from src.category import Category
from src.product import Product

if __name__ == "__main__":
    product1 = Product(
        "Samsung Galaxy S23 Ultra", "256GB, Серый цвет, 200MP камера", 180000.0, 5
    )
    product2 = Product("Iphone 15", "512GB, Gray space", 210000.0, 8)
    product3 = Product("Xiaomi Redmi Note 11", "1024GB, Синий", 31000.0, 14)

    category1 = Category(
        "Смартфоны",
        "Смартфоны, как средство не только коммуникации, но и получения "
        "дополнительных функций для удобства жизни",
        [product1, product2, product3],
    )

    # Проверяем работу геттера .products (Задание 2)
    print(category1.products)

    product4 = Product("55\" QLED 4K", "Фоновая подсветка", 123000.0, 7)
    category1.add_product(product4)

    # Проверяем добавление нового товара (Задание 1)
    print(category1.products)
    print(category1.product_count)

    # Проверяем фабричный класс-метод (Задание 3)
    new_product = Product.new_product(
        {
            "name": "Samsung Galaxy S23 Ultra",
            "description": "256GB, Серый цвет, 200MP камера",
            "price": 180000.0,
            "quantity": 5,
        }
    )
    print(new_product.name)
    print(new_product.description)
    print(new_product.price)
    print(new_product.quantity)

    # Проверяем интерактивное снижение цены (Доп. задание к Заданию 4)
    # Здесь программа приостановит работу и попросит ввести y/n в консоли!
    new_product.price = 800
    print(new_product.price)

    # Проверяем защиту от отрицательной и нулевой цены (Задание 4)
    new_product.price = -100
    print(new_product.price)
    new_product.price = 0
    print(new_product.price)
