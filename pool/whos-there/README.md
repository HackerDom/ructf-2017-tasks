# Who's there?

+ __Автор:__ m_messiah
+ __Описание:__ port-knock: По стуку на определенный порт - открываем следующий, и так пока через ascii из номеров портов не выдадим флаг.
+ __Текст задания:__
  ```
  - Who's there?
  - Maya
  - Maya who?
  - Maya hee, Maya ha-ha. (whos-there.tasks.ructf.org)
  
  В флаге нет части RuCTF: 
  ```
+ __Флаг:__ `DoItAg4iN!`
+ __Требования:__ Белый адрес для port-knocking (либо та же локальная сеть). Возможность доступа к портам: 1068,1111,1073,1116,1065,1103,1052,1105,1078,1033
+ __Настройка:__
  - Поставить knockd, использовать приложенный конфиг.
  - Поставить iptables, использовать приложенный конфиг.
+ __Решение:__
  - Посмотреть доступные порты - их три 1068, 1111, 1073
  - Использовать port-knocking и постучаться на них
  - Увидеть, что среди доступных портов появился еще один. Постучаться на три последних.
  - Повторить операцию, стуча в тройки портов, пока открываются всё новые.
  - Из каждого порта вычесть 1000 и преобразовать в ASCII.