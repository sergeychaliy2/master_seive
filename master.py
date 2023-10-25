import multiprocessing
import os

if __name__ == "__main__":
    url = input("Enter the URL: ")
    specific_words = input("Enter words: ").split(',')

    # Запуск слейвов параллельно
    with multiprocessing.Pool(processes=2) as pool:
        result1 = pool.apply_async(os.system, ("python slave1.py",))
        result2 = pool.apply_async(os.system, ("python slave2.py",))

    # Получение результатов
    result1.get()
    result2.get()
