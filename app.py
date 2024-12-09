import json


class User:
    def __init__(self, username, password, role):
        self.username = username
        self.password = password
        self.role = role


class Property:
    def __init__(self, id, address, price, type):
        self.id = id
        self.address = address
        self.price = price
        self.type = type


class RealEstateApp:
    def __init__(self):
        self.users = {}
        self.properties = []
        self.current_user = None
        self.load_data()

    def load_data(self):
        try:
            with open('data.json', 'r') as f:
                data = json.load(f)
                self.properties = [Property(**prop) for prop in data.get('properties', [])]
                self.users = {user['username']: User(**user) for user in data.get('users', [])}
        except FileNotFoundError:
            print("Файл данных не найден. Создан новый файл.")
            self.save_data()
        except json.JSONDecodeError:
            print("Ошибка чтения данных. Файл поврежден, создается новый файл.")
            self.save_data()

    def save_data(self):
        data = {
            'properties': [vars(prop) for prop in self.properties],
            'users': [vars(user) for user in self.users.values()]
        }
        with open('data.json', 'w') as f:
            json.dump(data, f)

    def register_user(self, username, password, role='user'):
        if username in self.users:
            print("Пользователь с таким именем уже существует.")
            return
        self.users[username] = User(username, password, role)
        self.save_data()
        print("Пользователь успешно зарегистрирован.")

    def login(self, username, password):
        user = self.users.get(username)
        if user and user.password == password:
            self.current_user = user
            print(f"Добро пожаловать, {username}!")
        else:
            print("Неверное имя пользователя или пароль.")

    def add_property(self, address, price, type):
        if self.current_user.role != 'admin':
            print("У вас нет прав для добавления недвижимости.")
            return
        property_id = len(self.properties) + 1
        new_property = Property(property_id, address, price, type)
        self.properties.append(new_property)
        self.save_data()
        print("Недвижимость успешно добавлена.")

    def view_properties(self):
        if not self.properties:
            print("Нет доступной недвижимости.")
            return
        for prop in self.properties:
            print(f"ID: {prop.id}, Адрес: {prop.address}, Цена: {prop.price}, Тип: {prop.type}")

    def delete_property(self, property_id):
        if self.current_user.role != 'admin':
            print("У вас нет прав для удаления недвижимости.")
            return
        self.properties = [prop for prop in self.properties if prop.id != property_id]
        self.save_data()
        print("Недвижимость успешно удалена.")

    def sort_properties(self, by='price'):
        if not self.properties:
            print("Нет доступной недвижимости для сортировки.")
            return
        if by == 'price':
            self.properties.sort(key=lambda x: x.price)
        elif by == 'address':
            self.properties.sort(key=lambda x: x.address)
        else:
            print("Неверный параметр сортировки. Используйте 'price' или 'address'.")
            return
        self.view_properties()

    def filter_properties(self, min_price=None, max_price=None):
        filtered = self.properties
        if min_price is not None:
            filtered = [prop for prop in filtered if prop.price >= min_price]
        if max_price is not None:
            filtered = [prop for prop in filtered if prop.price <= max_price]
        if not filtered:
            print("Нет недвижимости, соответствующей заданным критериям.")
            return
        for prop in filtered:
            print(f"ID: {prop.id}, Адрес: {prop.address}, Цена: {prop.price}, Тип: {prop.type}")


def main():
    app = RealEstateApp()

    # Создание администратора по умолчанию
    if 'admin' not in app.users:
        app.register_user('admin', 'password', 'admin')  # Логин: admin, Пароль: password

    while True:
        print("\n1. Регистрация")
        print("2. Вход")
        print("3. Выход")
        choice = input("Выберите действие: ")

        if choice == '1':
            username = input("Введите имя пользователя: ")
            password = input("Введите пароль: ")
            app.register_user(username, password)
        elif choice == '2':
            username = input("Введите имя пользователя: ")
            password = input("Введите пароль: ")
            app.login(username, password)

            while app.current_user:
                print("\n1. Добавить недвижимость")
                print("2. Просмотреть недвижимость")
                print("3. Удалить недвижимость")
                print("4. Сортировать недвижимость")
                print("5. Фильтровать недвижимость")
                print("6. Выйти")
                action = input("Выберите действие: ")

                if action == '1':
                    address = input("Введите адрес: ")
                    try:
                        price = float(input("Введите цену: "))
                        type = input("Введите тип недвижимости: ")
                        app.add_property(address, price, type)
                    except ValueError:
                        print("Ошибка: цена должна быть числом.")
                elif action == '2':
                    app.view_properties()
                elif action == '3':
                    try:
                        property_id = int(input("Введите ID недвижимости для удаления: "))
                        app.delete_property(property_id)
                    except ValueError:
                        print("Ошибка: ID должен быть числом.")
                elif action == '4':
                    by = input("Сортировать по (price/address): ")
                    app.sort_properties(by)
                elif action == '5':
                    try:
                        min_price = input("Минимальная цена (оставьте пустым для пропуска): ")
                        max_price = input("Максимальная цена (оставьте пустым для пропуска): ")
                        min_price = float(min_price) if min_price else None
                        max_price = float(max_price) if max_price else None
                        app.filter_properties(min_price, max_price)
                    except ValueError:
                        print("Ошибка: цена должна быть числом.")
                elif action == '6':
                    app.current_user = None
        elif choice == '3':
            break
        else:
            print("Неверный выбор. Пожалуйста, попробуйте снова.")


if __name__ == "__main__":
    main()

