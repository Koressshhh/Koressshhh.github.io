# Koressshhh.github.io

# Городской сад — ЛР5

Продолжение сайта лабораторной работы №4. Исходник сохранён коммитом 8f64d80.

Сайт: https://koressshhh.github.io/

Ветки: main, feature/photos, feature/form. В main исправлены контраст календаря и мобильное меню. В feature/photos добавлены три локальные фотографии. В feature/form добавлена проверка демонстрационной формы. Обе ветки объединены с main отдельными merge-коммитами через PR №1 и №2 и сохранены.

Форма не отправляет данные. Источники фотографий: IMAGE_SOURCES.md. Задания, по которым агент выполнял доработки: PROMPTS.md.

Сайт работает без сборки, изображения находятся в assets/images. GitHub Pages публикует сайт из артефакта собственного workflow .github/workflows/deploy.yml при каждом push в main.


## ЛР6 — автоматизация публикации

[![Deploy static site](https://github.com/Koressshhh/Koressshhh.github.io/actions/workflows/deploy.yml/badge.svg)](https://github.com/Koressshhh/Koressshhh.github.io/actions/workflows/deploy.yml)

Событие push в main запускает проверку, сборку папки _site и публикацию на GitHub Pages. Ручной запуск доступен дополнительно, но для проверки автодеплоя не используется.

Индивидуальный проект: перед деплоем выполняется `python3 scripts/check_site.py`. Проверяются вложенность HTML-тегов, уникальность id, один h1, title, подключение style.css, alt изображений, наличие локальных файлов и разделов, баланс фигурных скобок CSS. Это базовая проверка проекта, а не полная проверка по стандартам HTML/CSS. При ошибке шаг завершается ненулевым кодом, поэтому публикация не выполняется.

Структура: index.html — страница; style.css — оформление; assets/images — фотографии; scripts/check_site.py — проверка; .github/workflows/deploy.yml — CI/CD. В артефакт публикации попадают только файлы сайта. История и архив ЛР5 сохранены.
