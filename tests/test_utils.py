import pytest
import json
from pathlib import Path

from main import Product, Category
from src.utils import load_data_from_json


class TestLoadDataFromJson:
    """Тесты для функции загрузки данных из JSON"""

    def test_load_data_success(self, tmp_path):
        """Проверка успешной загрузки данных"""
        # Создание тестового JSON файла
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

        json_file = tmp_path / "test_products.json"
        with json_file.open('w', encoding='utf-8') as f:
            json.dump(test_data, f, ensure_ascii=False)

        # Сброс счетчиков
        Category.category_count = 0
        Category.product_count = 0

        # Загрузка данных
        categories = load_data_from_json(str(json_file))

        assert len(categories) == 1
        assert categories[0].name == "Смартфоны"
        assert len(categories[0].products) == 2
        assert Category.category_count == 1
        assert Category.product_count == 2

    def test_load_data_file_not_found(self):
        """Проверка обработки отсутствующего файла"""
        categories = load_data_from_json("nonexistent.json")
        assert categories == []

    def test_load_data_invalid_json(self, tmp_path):
        """Проверка обработки невалидного JSON"""
        invalid_file = tmp_path / "invalid.json"
        invalid_file.write_text("{invalid json", encoding='utf-8')

        categories = load_data_from_json(str(invalid_file))
        assert categories == []