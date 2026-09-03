import json
from src.utils import load_data_from_json
from src.category import Category


def test_load_data_success(tmp_path):
    """Проверка успешной загрузки данных"""
    # 1. Создание тестового словаря
    test_data = [
        {
            "name": "Смартфоны",
            "description": "Описание смартфонов",
            "products": [
                {
                    "name": "Samsung Galaxy S23 Ultra",
                    "description": "256GB, Серый цвет",
                    "price": 180000.0,
                    "quantity": 5
                },
                {
                    "name": "Iphone 15",
                    "description": "512GB, Gray space",
                    "price": 210000.0,
                    "quantity": 8
                }
            ]
        }
    ]

    # 2. Создаем файл во временной папке (вот она, переменная json_file!)
    json_file = tmp_path / "test_products.json"
    with json_file.open('w', encoding='utf-8') as f:
        json.dump(test_data, f, ensure_ascii=False)

    # 3. Сброс счетчиков перед тестом
    Category.category_count = 0
    Category.product_count = 0

    # 4. Загрузка данных из созданного json_file
    categories = load_data_from_json(str(json_file))

    # 5. Финальные проверки
    assert len(categories) == 1
    assert categories[0].name == "Смартфоны"

    # Проверяем текст, который теперь выдает наш геттер .products
    expected_products_output = (
        "Samsung Galaxy S23 Ultra, 180000.0 руб. Остаток: 5 шт.\n"
        "Iphone 15, 210000.0 руб. Остаток: 8 шт."
    )
    assert categories[0].products == expected_products_output
