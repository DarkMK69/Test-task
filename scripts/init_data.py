#!/usr/bin/env python3
import sys
import os
import time

# Добавляем корневую директорию в PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from sqlalchemy.orm import Session
from app.database import engine, Base, SessionLocal
from app.models import Category, Product, Client, Order, OrderItem, CategoryClosure

def init_test_data():
    """Инициализация тестовых данных"""
    print("🔄 Создание таблиц БД...")
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        # Проверяем, есть ли уже данные
        existing_categories = db.query(Category).count()
        if existing_categories > 0:
            print("✅ Данные уже существуют, пропускаем инициализацию")
            return
        
        print("🔄 Создание тестовых данных...")
        
        # Создаем категории
        home_appliances = Category(name="Бытовая техника")
        washing_machines = Category(name="Стиральные машины", parent=home_appliances)
        refrigerators = Category(name="Холодильники", parent=home_appliances)
        single_chamber = Category(name="однокамерные", parent=refrigerators)
        double_chamber = Category(name="двухкамерные", parent=refrigerators)
        tvs = Category(name="Телевизоры", parent=home_appliances)
        
        computers = Category(name="Компьютеры")
        laptops = Category(name="Ноутбуки", parent=computers)
        laptop_17 = Category(name="17\"", parent=laptops)
        laptop_19 = Category(name="19\"", parent=laptops)
        monoblocks = Category(name="Моноблоки", parent=computers)
        
        db.add_all([
            home_appliances, washing_machines, refrigerators, 
            single_chamber, double_chamber, tvs,
            computers, laptops, laptop_17, laptop_19, monoblocks
        ])
        db.commit()
        
        print("✅ Категории созданы")
        
        # Создаем closure table записи
        def build_closure(category, depth=0):
            closure = CategoryClosure(
                ancestor_id=category.id,
                descendant_id=category.id,
                depth=depth
            )
            db.add(closure)
            
            if category.parent:
                parent_closure = db.query(CategoryClosure).filter(
                    CategoryClosure.descendant_id == category.parent_id
                ).all()
                
                for pc in parent_closure:
                    new_closure = CategoryClosure(
                        ancestor_id=pc.ancestor_id,
                        descendant_id=category.id,
                        depth=pc.depth + 1
                    )
                    db.add(new_closure)
        
        # Строим closure table для всех категорий
        categories = db.query(Category).all()
        for category in categories:
            build_closure(category)
        
        db.commit()
        print("✅ Closure table построена")
        
        # Создаем продукты
        products = [
            Product(name="Стиральная машина Samsung", quantity=10, price=25000.00, category=washing_machines),
            Product(name="Холодильник однокамерный Bosh", quantity=5, price=18000.00, category=single_chamber),
            Product(name="Холодильник двухкамерный LG", quantity=8, price=32000.00, category=double_chamber),
            Product(name="Ноутбук 17\" Dell", quantity=15, price=45000.00, category=laptop_17),
            Product(name="Ноутбук 19\" HP", quantity=12, price=52000.00, category=laptop_19),
            Product(name="Моноблок Apple iMac", quantity=7, price=89000.00, category=monoblocks),
        ]
        
        db.add_all(products)
        db.commit()
        print("✅ Товары созданы")
        
        # Создаем клиентов
        clients = [
            Client(name="Иванов Иван", address="Москва, ул. Ленина, 1"),
            Client(name="Петров Петр", address="Санкт-Петербург, Невский пр., 10"),
        ]
        
        db.add_all(clients)
        db.commit()
        print("✅ Клиенты созданы")
        
        # Создаем заказы
        client1 = db.query(Client).filter(Client.name == "Иванов Иван").first()
        client2 = db.query(Client).filter(Client.name == "Петров Петр").first()
        
        orders = [
            Order(client_id=client1.id),
            Order(client_id=client2.id),
        ]
        
        db.add_all(orders)
        db.commit()
        print("✅ Заказы созданы")
        
        print("✅ Все тестовые данные успешно созданы!")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Ошибка при создании тестовых данных: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    # Даем время БД запуститься
    time.sleep(2)
    init_test_data()