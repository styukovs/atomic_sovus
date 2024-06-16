## Чтобы развернуть приложение нужно
- склонировать репозиторий `git clone https://github.com/styukovs/atomic_sovus.git`
- скопировать из яндекс диска архивы `vectorstores`, `data`
- разархивировать `vectorstores` в папку `./vectorstores` в корень проекта
- разархивировать `data` в папку `./data` в корень проекта
- собрать образ `docker build --tag sovus .`
- запустить контейнер `docker run --rm -p 8501:8501 --name sovus sovus:latest`

[Ссылка на яндекс диск](https://disk.yandex.ru/d/bDU3C5-AwE1pyg)

[Ссылка на развернутое решение](http://51.250.99.117:8501/)
