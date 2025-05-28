import psycopg2
import matplotlib.pyplot as plt

def main():
    # Подключение к базе данных
    conn = psycopg2.connect(
        dbname="medical_db",
        user="postgres",
        password="1",
        host="localhost",
        port="5432"
    )
    cur = conn.cursor()

    # Задание 2: Добавление новых приемов
    new_appointments = [
        (3, '2023-10-04'),
        (1, '2023-10-05')
    ]
    for app in new_appointments:
        cur.execute(
            "INSERT INTO appointments (doctor_id, date) VALUES (%s, %s)",
            (app[0], app[1])
        )
    conn.commit()
    print("✅ Данные о приемах добавлены")

    # Задание 3: Получение неврологов
    cur.execute("SELECT * FROM doctors WHERE specialization = 'Neurologist'")
    neurologists = cur.fetchall()
    print("\n🧑⚕️ Врачи-неврологи:")
    for doc in neurologists:
        print(f"ID: {doc[0]}, Имя: {doc[1]}, Больница: {doc[3]}")

    # Задание 4: Визуализация распределения врачей
    cur.execute("SELECT hospital, COUNT(*) FROM doctors GROUP BY hospital")
    hospitals_data = cur.fetchall()
    hospitals = [row[0] for row in hospitals_data]
    doctors_count = [row[1] for row in hospitals_data]

    plt.bar(hospitals, doctors_count)
    plt.title("Распределение врачей по больницам")
    plt.xlabel("Больница")
    plt.ylabel("Количество врачей")
    plt.show()

    # Задание 5: Анализ возраста пациентов
    cur.execute("""
        CREATE TABLE IF NOT EXISTS age_distribution (
            age_group VARCHAR(20) PRIMARY KEY,
            count INT
        )
    """)
    cur.execute("DELETE FROM age_distribution")
    
    # Группировка по возрастным категориям
    age_bins = [0, 18, 35, 60, 100]
    labels = ['0-18', '19-35', '36-60', '60+']
    
    cur.execute("SELECT age FROM patients")
    ages = [row[0] for row in cur.fetchall()]
    
    # Создание гистограммы
    plt.hist(ages, bins=age_bins, edgecolor='black')
    plt.title("Распределение пациентов по возрасту")
    plt.xlabel("Возрастные группы")
    plt.ylabel("Количество пациентов")
    plt.xticks(age_bins, labels)
    plt.show()

    # Заполнение таблицы age_distribution
    for label in labels:
        cur.execute("""
            INSERT INTO age_distribution (age_group, count)
            VALUES (%s, %s)
        """, (label, 0))
    
    cur.execute("""
        UPDATE age_distribution SET count = 
            CASE 
                WHEN age_group = '0-18' THEN (SELECT COUNT(*) FROM patients WHERE age BETWEEN 0 AND 18)
                WHEN age_group = '19-35' THEN (SELECT COUNT(*) FROM patients WHERE age BETWEEN 19 AND 35)
                WHEN age_group = '36-60' THEN (SELECT COUNT(*) FROM patients WHERE age BETWEEN 36 AND 60)
                WHEN age_group = '60+' THEN (SELECT COUNT(*) FROM patients WHERE age > 60)
            END
    """)
    conn.commit()
    print("\n📊 Таблица age_distribution обновлена")

    cur.close()
    conn.close()

if __name__ == "__main__":
    main()