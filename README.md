<p align="center">
  <img src="pics/XINZINVPN.png" alt="XinZin VPN" width="600">
</p>

# XinZin VPN

## 🇷🇺 Русский (Ru)

### О проекте

**XinZin VPN** — это агрегированная VPN-подписка, объединяющая серверы из нескольких популярных открытых конфигураций:

1. `AetrisVPN`
2. `NosokVPN`
3. `Subzio`
4. `FlareFeed`
5. `IgareckVPN`
6. `Luxxuria`

### Как это работает?

Для обеспечения качества и актуальности списка серверов используется несколько этапов фильтрации и проверки.

**1. Удаление дубликатов**

На первом этапе производится сбор серверов из всех источников и удаление повторяющихся конфигураций.

**2. TCP Ping**

После очистки выполняется проверка TCP-соединения. Она позволяет предварительно оценить доступность серверов и отсеять некоторые неработающие или некорректные конфигурации.

**3. URL Test**

Затем запускается URL Test, который проверяет возможность передачи данных через сервер и определяет время отклика (Ping).

**4. Определение местоположения**

После завершения проверок серверам присваиваются соответствующие флаги стран в зависимости от их предполагаемого географического расположения.

Если определить местоположение не удаётся, вместо флага отображается 🇽🇽.

### Как пользоваться подпиской?

XinZin VPN поддерживает клиенты, работающие с подписками формата V2Ray / sing-box, включая NekoBox, Throne и HAPP.

**Общая инструкция по добавлению подписки:**

1. Скопируйте URL-адрес подписки XinZin VPN.
2. Откройте используемый VPN-клиент.
3. Найдите раздел управления профилями или подписками.
4. Выберите добавление подписки по URL (Import from URL / Add Subscription).
5. Вставьте скопированную ссылку и сохраните её.
6. Запустите обновление подписки, чтобы загрузить список серверов.
7. Выберите подходящий сервер и подключитесь к нему.

**NekoBox:**
- Откройте приложение.
- Перейдите в раздел конфигураций.
- Нажмите `+` и выберите импорт из URL.
- Вставьте ссылку на подписку и подтвердите добавление.
- Обновите конфигурацию и выберите сервер.

**Throne / HAPP:**
- Откройте приложение.
- Найдите раздел профилей или подписок.
- Добавьте новую подписку через URL.
- Вставьте ссылку и сохраните профиль.
- Обновите список серверов и подключитесь к выбранному.

*Названия пунктов меню могут отличаться в зависимости от версии приложения.*

### Важная информация о стабильности

XinZin VPN зависит от сторонних проектов и используемых ими источников серверов. Поэтому стабильная работа подписки и постоянная доступность всех серверов не гарантируются.

Серверы могут переставать работать, удаляться или изменяться без предварительного уведомления. Результаты TCP Ping и URL Test также не гарантируют дальнейшую работоспособность сервера.

Определение географического местоположения серверов может быть неточным. Отображаемые флаги стран не всегда соответствуют фактическому расположению серверов.

### Примечания

P.S.
Проект находится в разработке. Новые подписки и тесты появятся в скором времени (Speed test).

Этот код был написан нейросетью, так как я не знаю Python и в целом не очень хорошо знаком с GitHub. Делаю эту подписку больше для себя, чем для остальных, но буду не против, если ей будут пользоваться другие.

### Ресурсы

**Исходные репозитории используемых подписок:**

- **IgareckVPN:** https://github.com/igareck/vpn-configs-for-russia
- **AetrisVPN:** https://github.com/flaafix/AetrisVPN
- **FlareFeed:** https://github.com/svinakraft-maker/FlareFeed
- **Subzio:** https://github.com/Subzio/subzio
- **NosokVPN:** https://github.com/aviamastersgh/vpn-free-russia
- **Luxxuria:** https://github.com/luxxuria/harvester

## 🇬🇧 English (En)

# About the Project

**XinZin VPN** is an aggregated VPN subscription that combines servers from several popular public VPN configurations:

1. `AetrisVPN`
2. `NosokVPN`
3. `Subzio`
4. `FlareFeed`
5. `IgareckVPN`
6. `Luxxuria`

### How does it work?

To maintain the quality and availability of the server list, several filtering and testing stages are performed.

**1. Duplicate Removal**

Servers are collected from all available sources, and duplicate configurations are removed.

**2. TCP Ping**

A TCP connection test is performed to check basic server accessibility and filter out some unavailable or incomplete configurations.

**3. URL Test**

Next, a URL Test is performed to verify whether data can be transferred through the server and to measure its response time (Ping).

**4. Geolocation**

Once testing is complete, country flags are assigned according to the servers' estimated geographical locations.

If the location cannot be determined, a 🇽🇽 icon is displayed instead.

### How to use the subscription

XinZin VPN supports VPN clients compatible with V2Ray / sing-box subscription formats, including NekoBox, Throne and HAPP.

**General setup instructions:**

1. Copy the XinZin VPN subscription URL.
2. Open your preferred VPN client.
3. Navigate to the profiles or subscription management section.
4. Select the option to import a subscription from a URL.
5. Paste the copied link and save it.
6. Update the subscription to download the server list.
7. Select a server and connect.

**NekoBox:**
- Open the application.
- Navigate to the configuration section.
- Tap `+` and select URL import.
- Paste the subscription URL and confirm.
- Update the configuration and select a server.

**Throne / HAPP:**
- Open the application.
- Navigate to profiles or subscriptions.
- Add a new subscription using its URL.
- Paste the link and save the profile.
- Update the server list and connect to your preferred server.

*Menu names and navigation may vary depending on the application version.*

### Important: Stability Notice

XinZin VPN depends on third-party projects and their server sources. Therefore, continuous subscription stability and the availability of all servers cannot be guaranteed.

Servers may stop working, be removed or change without prior notice. TCP Ping and URL Test results do not guarantee continued server availability.

Server geolocation may also be inaccurate. Displayed country flags may not always reflect the actual server location.

### Notes

P.S.  
The project is still under development.
New subscriptions and tests will be added soon (Speed test)  
This code was written by an AI because I don't know Python and am generally not very familiar with GitHub. I'm making this subscription more for myself than for anyone else, but I don't mind if others use it.

### Resources

**Source repositories:**

- **IgareckVPN:** https://github.com/igareck/vpn-configs-for-russia
- **AetrisVPN:** https://github.com/flaafix/AetrisVPN
- **FlareFeed:** https://github.com/svinakraft-maker/FlareFeed
- **Subzio:** https://github.com/Subzio/subzio
- **NosokVPN:** https://github.com/aviamastersgh/vpn-free-russia
- **Luxxuria:** https://github.com/luxxuria/harvester

## 🇮🇷 فارسی (Fa)

# درباره پروژه

**XinZin VPN** یک اشتراک تجمیعی VPN است که سرورهای چندین کانفیگ عمومی و محبوب را در یک مجموعه گردآوری می‌کند:

1. `AetrisVPN`
2. `NosokVPN`
3. `Subzio`
4. `FlareFeed`
5. `IgareckVPN`
6. `Luxxuria`

### این پروژه چگونه کار می‌کند؟

برای حفظ کیفیت و به‌روز بودن فهرست سرورها، چند مرحله فیلتر و آزمایش انجام می‌شود.

**۱. حذف موارد تکراری**

ابتدا سرورها از تمام منابع جمع‌آوری شده و کانفیگ‌های تکراری حذف می‌شوند.

**۲. TCP Ping**

در این مرحله اتصال TCP بررسی می‌شود تا دسترسی اولیه به سرورها ارزیابی و برخی کانفیگ‌های غیرفعال یا ناقص حذف شوند.

**۳. URL Test**

سپس با استفاده از URL Test، امکان انتقال داده از طریق سرور بررسی و زمان پاسخ‌گویی (Ping) اندازه‌گیری می‌شود.

**۴. تشخیص موقعیت جغرافیایی**

پس از پایان آزمایش‌ها، بر اساس موقعیت جغرافیایی تخمینی سرورها، پرچم کشور مربوطه به آن‌ها اختصاص داده می‌شود.

اگر موقعیت سرور قابل تشخیص نباشد، به‌جای پرچم از نماد 🇽🇽 استفاده می‌شود.

### چگونه از اشتراک استفاده کنیم؟

XinZin VPN با کلاینت‌هایی که از فرمت‌های اشتراک V2Ray / sing-box پشتیبانی می‌کنند، از جمله NekoBox، Throne و HAPP سازگار است.

**راهنمای کلی:**

۱. لینک اشتراک XinZin VPN را کپی کنید.  
۲. برنامه VPN موردنظر خود را باز کنید.  
۳. وارد بخش پروفایل‌ها یا اشتراک‌ها شوید.  
۴. گزینه افزودن اشتراک از طریق URL را انتخاب کنید.  
۵. لینک کپی‌شده را وارد کرده و ذخیره کنید.  
۶. اشتراک را به‌روزرسانی کنید تا فهرست سرورها دریافت شود.  
۷. سرور موردنظر را انتخاب کرده و متصل شوید.

**NekoBox:**
- برنامه را باز کنید.
- وارد بخش کانفیگ‌ها شوید.
- روی `+` بزنید و گزینه وارد کردن از URL را انتخاب کنید.
- لینک اشتراک را وارد و تأیید کنید.
- کانفیگ‌ها را به‌روزرسانی کرده و سرور دلخواه را انتخاب کنید.

**Throne / HAPP:**
- برنامه را باز کنید.
- به بخش پروفایل‌ها یا اشتراک‌ها بروید.
- یک اشتراک جدید از طریق URL اضافه کنید.
- لینک را وارد و ذخیره کنید.
- فهرست سرورها را به‌روزرسانی کرده و متصل شوید.

*نام گزینه‌ها ممکن است بسته به نسخه برنامه متفاوت باشد.*

### اطلاعات مهم درباره پایداری

XinZin VPN به پروژه‌های شخص ثالث و منابع سرور آن‌ها وابسته است. بنابراین، پایداری دائمی اشتراک و عملکرد بدون مشکل تمام سرورها تضمین نمی‌شود.

سرورها ممکن است بدون اطلاع قبلی از کار بیفتند، حذف شوند یا تغییر کنند. نتایج TCP Ping و URL Test نیز عملکرد مداوم سرورها را تضمین نمی‌کنند.

تشخیص موقعیت جغرافیایی سرورها ممکن است دقیق نباشد و پرچم‌های نمایش‌داده‌شده همیشه نشان‌دهنده موقعیت واقعی سرورها نیستند.

### یادداشت‌ها

P.S.  
پروژه هنوز در حال توسعه است.
اشتراک‌های جدید و آزمایش‌های بیشتری به‌زودی اضافه خواهند شد (Speed test)  
این کد توسط هوش مصنوعی نوشته شده است، زیرا من با پایتون آشنایی ندارم و به‌طور کلی تجربه زیادی در کار با GitHub ندارم. این اشتراک را بیشتر برای استفاده شخصی خودم تهیه می‌کنم، اما از استفاده دیگران از آن نیز استقبال می‌کنم.

### منابع

**مخازن اصلی پروژه‌های مورد استفاده:**

- **IgareckVPN:** https://github.com/igareck/vpn-configs-for-russia
- **AetrisVPN:** https://github.com/flaafix/AetrisVPN
- **FlareFeed:** https://github.com/svinakraft-maker/FlareFeed
- **Subzio:** https://github.com/Subzio/subzio
- **NosokVPN:** https://github.com/aviamastersgh/vpn-free-russia
- **Luxxuria:** https://github.com/luxxuria/harvester

## 🇹🇷 Türkçe (Tr)

# Proje Hakkında

**XinZin VPN**, birçok popüler ve herkese açık VPN yapılandırmasındaki sunucuları tek bir abonelikte birleştiren bir VPN projesidir.

Kullanılan kaynaklar:

1. `AetrisVPN`
2. `NosokVPN`
3. `Subzio`
4. `FlareFeed`
5. `IgareckVPN`
6. `Luxxuria`

### Nasıl çalışır?

Sunucu listesinin kalitesini ve güncelliğini korumak için birkaç filtreleme ve test aşaması uygulanır.

**1. Yinelenen Sunucuların Kaldırılması**

İlk olarak tüm kaynaklardan sunucular toplanır ve aynı yapılandırmaya sahip tekrar eden sunucular kaldırılır.

**2. TCP Ping**

Sunucuların temel bağlantı durumu kontrol edilir. Bu işlem, erişilemeyen veya eksik yapılandırmalara sahip bazı sunucuların elenmesini sağlar.

**3. URL Test**

Ardından URL Test gerçekleştirilir. Bu test, sunucu üzerinden veri aktarımının mümkün olup olmadığını kontrol eder ve yanıt süresini (Ping) ölçer.

**4. Coğrafi Konum Belirleme**

Testler tamamlandıktan sonra sunucuların tahmini coğrafi konumlarına göre ülke bayrakları atanır.

Sunucunun konumu belirlenemezse ülke bayrağı yerine 🇽🇽 simgesi gösterilir.

### Abonelik nasıl kullanılır?

XinZin VPN; NekoBox, Throne ve HAPP dahil olmak üzere V2Ray / sing-box abonelik formatlarını destekleyen VPN istemcileriyle uyumludur.

**Genel kurulum rehberi:**

1. XinZin VPN abonelik bağlantısını kopyalayın.
2. Kullandığınız VPN uygulamasını açın.
3. Profil veya abonelik yönetimi bölümüne gidin.
4. URL üzerinden abonelik ekleme seçeneğini seçin.
5. Kopyaladığınız bağlantıyı yapıştırıp kaydedin.
6. Sunucu listesini indirmek için aboneliği güncelleyin.
7. İstediğiniz sunucuyu seçerek bağlantı kurun.

**NekoBox:**
- Uygulamayı açın.
- Yapılandırmalar bölümüne gidin.
- `+` simgesine dokunun ve URL üzerinden içe aktarma seçeneğini seçin.
- Abonelik bağlantısını yapıştırıp onaylayın.
- Yapılandırmayı güncelleyin ve bir sunucu seçin.

**Throne / HAPP:**
- Uygulamayı açın.
- Profil veya abonelikler bölümüne gidin.
- URL kullanarak yeni bir abonelik ekleyin.
- Bağlantıyı yapıştırıp kaydedin.
- Sunucu listesini güncelleyerek istediğiniz sunucuya bağlanın.

*Menü adları uygulama sürümüne göre değişiklik gösterebilir.*

### Kararlılık Hakkında Önemli Bilgi

XinZin VPN, üçüncü taraf projelere ve onların sunucu kaynaklarına bağlıdır. Bu nedenle aboneliğin sürekli kararlı çalışması ve tüm sunucuların kullanılabilirliği garanti edilemez.

Sunucular önceden haber verilmeksizin çalışmayı durdurabilir, kaldırılabilir veya değiştirilebilir. TCP Ping ve URL Test sonuçları da sunucuların sürekli çalışacağını garanti etmez.

Sunucuların coğrafi konumları yanlış tespit edilebilir. Gösterilen ülke bayrakları her zaman sunucuların gerçek konumunu yansıtmayabilir.

### Notlar

P.S.  
Proje geliştirme aşamasındadır.
Yakında yeni abonelikler ve testler eklenecektir (Speed test)  
Bu kod, Python bilmediğim ve genel olarak GitHub konusunda deneyimim olmadığı için yapay zekâ tarafından yazılmıştır. Bu aboneliği öncelikle kendim kullanmak için hazırlıyorum, ancak başkalarının da kullanmasına karşı değilim.

### Kaynaklar

**Kullanılan aboneliklerin kaynak depoları:**

- **IgareckVPN:** https://github.com/igareck/vpn-configs-for-russia
- **AetrisVPN:** https://github.com/flaafix/AetrisVPN
- **FlareFeed:** https://github.com/svinakraft-maker/FlareFeed
- **Subzio:** https://github.com/Subzio/subzio
- **NosokVPN:** https://github.com/aviamastersgh/vpn-free-russia
- **Luxxuria:** https://github.com/luxxuria/harvester

## 🇨🇳 简体中文 (Zh-CN)

# 关于项目

**XinZin VPN** 是一个聚合型 VPN 订阅项目，将多个热门公开配置中的服务器整合到一个订阅中。

目前使用的来源包括：

1. `AetrisVPN`
2. `NosokVPN`
3. `Subzio`
4. `FlareFeed`
5. `IgareckVPN`
6. `Luxxuria`

### 工作原理

为了保证服务器列表的质量和可用性，项目会执行多个筛选和测试步骤。

**1. 去重**

首先从所有来源收集服务器，并删除重复的配置。

**2. TCP Ping**

随后进行 TCP 连接测试，初步检查服务器的可访问性，并筛除部分不可用或配置不完整的节点。

**3. URL Test**

接下来执行 URL Test，检查服务器是否能够正常传输数据，并测量响应延迟（Ping）。

**4. 地理位置识别**

所有测试完成后，根据服务器推测的地理位置为其分配对应的国家或地区旗帜。

如果无法识别服务器的位置，则显示 🇽🇽 图标，而不是国家旗帜。

### 如何使用订阅？

XinZin VPN 兼容支持 V2Ray / sing-box 订阅格式的客户端，包括 NekoBox、Throne 和 HAPP。

**通用使用教程：**

1. 复制 XinZin VPN 的订阅链接。
2. 打开你使用的 VPN 客户端。
3. 进入配置文件或订阅管理页面。
4. 选择通过 URL 添加订阅。
5. 粘贴订阅链接并保存。
6. 更新订阅以获取服务器列表。
7. 选择一个服务器并连接。

**NekoBox：**
- 打开应用。
- 进入配置页面。
- 点击 `+`，选择通过 URL 导入。
- 粘贴订阅链接并确认。
- 更新配置，然后选择服务器。

**Throne / HAPP：**
- 打开应用。
- 进入配置文件或订阅页面。
- 通过 URL 添加新的订阅。
- 粘贴链接并保存。
- 更新服务器列表，然后选择服务器连接。

*不同版本的应用可能使用不同的菜单名称。*

### 稳定性重要说明

XinZin VPN 依赖第三方项目及其服务器来源，因此无法保证订阅始终稳定，也无法保证所有服务器持续可用。

服务器可能在没有提前通知的情况下停止工作、被移除或发生变化。TCP Ping 和 URL Test 的测试结果也不代表服务器能够持续正常运行。

服务器的地理位置识别可能存在误差，显示的国家旗帜不一定与服务器的实际所在地相符。

### 说明

P.S.  
项目仍在开发中。
新的订阅源和测试功能将在近期推出（Speed test）  
这段代码是由人工智能编写的，因为我不懂 Python，而且总体来说对 GitHub 也不熟悉。我创建这个订阅主要是为了自己使用，不过也欢迎其他人使用。

### 资源

**所使用订阅的源代码仓库：**

- **IgareckVPN:** https://github.com/igareck/vpn-configs-for-russia
- **AetrisVPN:** https://github.com/flaafix/AetrisVPN
- **FlareFeed:** https://github.com/svinakraft-maker/FlareFeed
- **Subzio:** https://github.com/Subzio/subzio
- **NosokVPN:** https://github.com/aviamastersgh/vpn-free-russia
- **Luxxuria:** https://github.com/luxxuria/harvester



Developed by Fafix
