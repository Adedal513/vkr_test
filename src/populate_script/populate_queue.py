import csv
import uuid
import random
import datetime
from randomtimestamp import randomtimestamp

PRODUCT_CATEGORIES = [
    "Электроника",
    "Бытовая техника",
    "Компьютеры и ноутбуки",
    "Мобильные телефоны",
    "Аксессуары для мобильных телефонов",
    "Одежда и обувь",
    "Дом и интерьер",
    "Красота и здоровье",
    "Продукты питания",
    "Книги и мультимедиа",
    "Товары для детей",
    "Спорт и отдых",
    "Автотовары",
    "Сад и огород",
    "Животные и товары для них",
    "Развлечения и хобби",
    "Услуги"
]
RECORDS_AMNT = 1000
START_DATE = datetime.datetime(2022, 1, 1)
END_DATE = datetime.datetime(2024, 4, 20)

def main():
    with open('labeled.csv') as f:
        reader = csv.reader(f)
        comments = [row[0] for row in reader]
    print(f'Считано {len(comments)} комментариев')

    dataset = []
    for i in range(RECORDS_AMNT):
        record = dict()

        record['message_id'] = str(uuid.uuid4())
        record['user_id'] = str(uuid.uuid4())
        record['text'] = comments[i]
        record['product_category'] = random.choice(PRODUCT_CATEGORIES)
        record['created_at'] = randomtimestamp(
            start=START_DATE,
            end=END_DATE,
            text=True
        )

        dataset.append(record)
    
    print(random.choice(dataset))



if __name__ == '__main__':
    main()