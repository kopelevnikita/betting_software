# betting_software
Test task (Betting Software)

## Структура
- Сервис [bet_maker](bet_maker), принимающий ставки на эти события от пользователя.
- Сервис-провайдер информации о событиях [link_provider](link_provider).

### Запуск приложения

1. Создайте .env файл в корневой директории проекта из примера .env.example.
2. Создайте .env файлы в сервисах bet_maker и link_provider из .env.example.global
3. Запустите команду `docker-compose up --build -d` для запуска всех необходимых контейнеров.

    ```sh
    docker-compose up --build -d
    ```
4. После успешного запуска сервис bet_maker будет доступен по адресу: http://localhost:8000, сервис 
link_provider по адресу: http://localhost:8001.

5. Документация будет доступна по адресу: http://localhost:8000/api/openapi и http://localhost:8001/api/openapi.
