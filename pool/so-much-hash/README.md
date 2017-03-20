# WOW! So much hash

+ __Автор:__ m_messiah
+ __Категория:__ stegano
+ __Описание:__ Локальный git-репо. Где-то в истории был файл с флагом.
+ __Текст участникам:__ Hashes! I like hashes! So much hashes! Which is mine? (ссылка на архив)
+ __Флаг:__ RuCTF: ReF1oGisSoHe1pFull
+ __Решение:__ `git grep RuCTF $(git reflog show | awk '{print $1}')`
