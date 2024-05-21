1. Определение проблемы

Существует необходимость в инструменте, который мог бы автоматически создавать визуализации для аудиофайлов и отправлять их пользователям. Такое решение было бы полезно для создателей контента, музыкантов и других пользователей, которые хотят быстро и просто получать анимированные видео из своих аудиозаписей.

2. Выработка требований (фич-лист)
Основные требования к Telegram-боту:

Принимать аудиофайлы в формате MP3 от пользователей.
Создавать визуализацию аудиофайла в формате видео.
Сжимать созданное видео для экономии места и трафика.
Отправлять сжатое видео обратно пользователю.
Обрабатывать только аудиофайлы с корректным MIME-типом.
Уведомлять пользователя об ошибках (например, если аудиофайл имеет неподдерживаемый формат).
3. Разработка архитектуры и проектирование
Архитектура бота:

Основной модуль (main.py): Содержит основной код бота и определяет обработчики сообщений.
Функция создания визуализации (create_visualization): Использует ffmpeg для генерации видео из аудиофайла.
Функция сжатия видео (compress_video): Использует библиотеку moviepy для сжатия видео.
Обработчики сообщений: Используют библиотеку aiogram для взаимодействия с Telegram API и обработки входящих сообщений и команд.
Тесты (tests/test_main.py): Содержат unit-тесты и интеграционные тесты для проверки функциональности.
4. Кодирование и отладка
Бот был реализован на Python с использованием библиотек aiogram для взаимодействия с Telegram API и moviepy для обработки видео. Основные функции были реализованы и протестированы локально.

5. Unit-тестирование
Были написаны unit-тесты для основных функций:

Тестирование функции create_visualization с использованием мока для subprocess.run.
Тестирование функции compress_video с использованием мока для VideoFileClip.
Тестирование обработчика сообщений process_audio.
