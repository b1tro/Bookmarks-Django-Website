# Bookmarks Django Website

Проект "Сохранёнки", написанный на Django, стили пытаются повторить дизайн старого "Вконтакте", название также дает отсылку на культуру ушедшего времени. Представляет из себя достаточно простой сайт - социальная сеть, в котором можно добавлять картинки из интернета в ленту. Картинки можно лайкать, на авторов подписываться. На сайте присутствует разная статистика.

Используемый стек: бэкенд - Django (API в том числе), базы данных - PostgreSQL, Redis, серваки - nginx, настроенный на раздачу static и media файлов, сам сайт на wsgi gunicorn.

Конфигурации настроены под компоуз контейнер, есть Dockerfile для Django-проекта, а также Docker-Compose.yml для использования nginx, redis, postgresql.

Автор - Михаил Назаров, почта mishanaz737@gmail.com, телеграм - https://t.me/conlentitudpoderosa

Важно: база данных пустая, для того чтобы в полной мере оценить функционал рекомендуется создать дополнительного пользователя и загрузить от него и админа несколько изображений на сайт. Данные от учетной записи админа: admin admin. 
Также не работает восстановление пароля по почте, так как из переменных окружения в целях безопасности были удалены хост и пароль.
