# Лабораторная работа №1 

### Исходные данные
• Цифровое изображение
• Алгоритм внесения искажений

### Общий план выполнения работы
1. Разработать клиент серверный механизм передачи цифрового изображения.
2. Учесть возможность возникновения помех в канале передачи.
3. Разработать блок восстановления полученных изображений на стороне сервера.
4. Для передачи данных между клиентом и сервером использовать сокеты Беркли.
5. Оценить потери данных при наличии блока восстановления ошибок и при его
отсутствии.

#### Описание программы
Программа состоит из трёх модулей:

Client - отвечает за отправку исходного изображения.

Noise_Server - промежуточный сервер, который принимает оригинальное изображение, добавляет к нему импульсный шум, и отправляет конечному серверу.

Server - принимает изображение с шумом и восстанавливает его, затем оцениват потери данных.

Передача между модулями осуществляется с помощью сокетов Беркли. Отдельно было прописано два метода: для внесения импульного шума (add_noise) и реализация медианного фильтра для его устранения (m_filter). В отличие от встроенного он меньше размывает изображение.

Для оценки потери данных считается стандартное отклонение и вычисляется процент незатронутых пикселей, где пиксель считается незатронутым, если его значение изменилось менее чем на 20.

### Результаты
Ниже приведена таблица, показывающая потери в случае когда изображение содержит шум и в случае когда оно было восстановлено.

Изображение | Стандартное отклонение | Незатронутые пиксели, % 
:----:|:-------:|:-----------:
С шумом | 45.04 | 89.97
Восстановленное | 9.98| 77.74

Изображение, передаваемое клиентом:

![](Art.jpg)

Изображение с шумом:

![](Art_noise.jpg)

Изображение после применения фильтра:

![](Result_art.jpg)
 
