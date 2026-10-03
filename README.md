<p align="center">
  <img src="panel-logo.png" alt="WIDUMPROXY" width="190">
</p>

<h1 align="center">WIDUMPROXY 2.4.5</h1>

<p align="center">WEB Proxy, MTProto, VLESS XHTTP, Hysteria2, OpenFlux и аккуратная панель управления для собственного VPS</p>

## Возможности

- Подписки и отдельные подключения с QR-кодами и готовыми конфигурациями.
- VLESS XHTTP и Hysteria2, включая прямые и CDN-подключения VLESS.
- Отдельные профили MTProto, Telegram Web Proxy и OpenFlux через Яндекс, Mail.ru или MAX для iOS и Android.
- Управление пользователями, ограничениями устройств, трафиком и состоянием служб.
- Объединение нескольких VPS в одну подписку через Node API token.
- Автоматическое определение страны и города ноды с отображением флага.
- Готовые HTML-заглушки и собственные страницы с HTML, CSS, JavaScript, SEO и аналитикой.
- Проверка обновлений и безопасное обновление с резервной копией настроек.

## Что нового в 2.4.5

- Окно создания отдельного подключения стало компактнее и понятнее на компьютере и телефоне.
- Для VLESS XHTTP, Hysteria2, MTProto и Web Proxy можно выдать от 1 до 20 отдельных ключей: у каждого есть собственная ссылка и QR-код.
- Добавлен лимит суммарного входящего и исходящего трафика отдельного подключения. Значение `0` означает работу без ограничения.
- После исчерпания квоты подключение автоматически отключается. Ручное повторное включение начинает новый период учёта без удаления накопленной статистики.
- Количество устройств означает число выданных персональных ключей. Это не аппаратная HWID-блокировка: не передавайте один ключ нескольким устройствам.


## Требования

- Чистый VPS с Ubuntu 22.04+, Ubuntu 24.04+ или Debian 12+.
- Архитектура `x86_64` и доступ пользователя `root`.
- Домен или поддомен с A-записью на публичный IPv4 сервера.
- Свободные и открытые `80/tcp` и `443/tcp`.

Перед установкой убедитесь, что домен уже указывает на сервер. Дополнительные порты выбранных подключений панель покажет автоматически; их также нужно открыть во внешнем firewall личного кабинета VPS-провайдера.

## Быстрый старт

Подключитесь к серверу по SSH и перейдите в режим `root`:

```bash
sudo -i
```

### Установка

```bash
apt-get -o DPkg::Lock::Timeout=600 install -y unzip && rm -rf /root/wpp-244-release && mkdir -p /root/wpp-244-release && unzip -q /root/WEB-PANEL-PROXY-V-2.4.5-RELEASE.zip -d /root/wpp-244-release && cd /root/wpp-244-release && chmod +x ./*.sh && bash ./install-final.sh
```

Перед запуском загрузите архив релиза в `/root`. Установщик запросит домен, email для HTTPS-сертификата, логин и пароль панели. После установки он покажет адрес панели и данные для входа.

### После установки

1. Сохраните адрес панели, логин, пароль и Node API token в безопасном месте.
2. Откройте показанный HTTPS-адрес панели и создайте пользователя или отдельное подключение.
3. Скачайте конфигурацию, скопируйте ссылку либо отсканируйте QR-код подходящим клиентом.
4. Для удалённой ноды установите эту же версию WPP на втором VPS и добавьте её Node API token во вкладке **Ноды**.

### Обновление

```bash
/usr/local/sbin/web-panel-proxy-update
```

Обновление устанавливает последний стабильный релиз и сохраняет пользователей, ключи, настройки, адрес панели и HTML-заглушки.

### Удаление

```bash
/usr/local/sbin/web-panel-proxy-uninstall
```

> **Внимание:** удаление выполняется без дополнительного подтверждения и стирает пользователей, ключи, конфигурации, службы и сайт WIDUMPROXY.

## Сеть и порты

| Назначение | Порт |
|---|---:|
| HTTP, выпуск сертификата и перенаправление на HTTPS | `80/tcp` |
| HTTPS, панель и защищённые подключения | `443/tcp` |
| Hysteria2 по умолчанию | `8443/udp` |
| MTProto | выбранный порт, обычно `2399–2430/tcp` |

Caddy постоянно использует `80/tcp` и `443/tcp`. Не запускайте на этих портах другой веб-сервер. Если используется UFW, панель добавит свои правила, но firewall у VPS-провайдера необходимо настроить отдельно.

## Проверка состояния

Открыть консольное меню:

```bash
WPP
```

Проверить службы и последние сообщения панели:

```bash
systemctl --failed --no-pager
journalctl -u tproxy-panel.service -n 100 --no-pager
```

Проверить занятые порты:

```bash
ss -lntup
```

## Полезно знать

- Адрес панели, Node API token и ссылки подключений являются секретными — не публикуйте их.
- Перед обновлением автоматически создаётся резервная копия.
- Для OpenFlux требуется отдельная публичная ссылка на документ Яндекса или Mail.ru для каждого пользователя.
- QR-код OpenFlux содержит данные доступа. Не публикуйте его и удаляйте профиль при потере устройства.
- OpenFlux работает как экспериментальный IPv4/TCP-туннель; UDP и IPv6 через него не передаются.
- Резервные копии могут содержать пароли и ключи — не загружайте их в публичный репозиторий.

## Ссылки

- [GitHub проекта](https://github.com/TETRIX8/widumproxy-panel)

## Лицензия

MIT License. Подробности находятся в файле [LICENSE](LICENSE).

## WidumProxy quick install

This repository is the GitHub distribution of WidumProxy v2.4.5. The installer keeps the full upstream functionality while using this repository as the source for initial installation and updates.

```bash
sudo -i bash -c 'curl -4fsSL "https://raw.githubusercontent.com/TETRIX8/widumproxy-panel/v2.4.5/install.sh" -o /tmp/widumproxy-install.sh && bash /tmp/widumproxy-install.sh; rc=$?; rm -f /tmp/widumproxy-install.sh; exit $rc'
```

Optional non-interactive environment variables:

- `WEB_PANEL_PROXY_DOMAIN` — public hostname for the panel.
- `WEB_PANEL_PROXY_ACME_EMAIL` — email for TLS certificate notifications.
- `WEB_PANEL_PROXY_REF` — GitHub tag or branch to install.
- `WEB_PANEL_PROXY_ALLOW_CDN=1` — allow installation when the hostname intentionally resolves to a CDN instead of the VPS IP.

The installer and updater retain the internal service names and filesystem paths for compatibility with existing deployments.
