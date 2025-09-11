# Comprehensive Test Script for All Stages
echo "=== COMPREHENSIVE VFS TERMINAL TEST ==="

# Показать информацию о VFS
vfs_info

# Навигация и просмотр
pwd
ls -l
cd documents
pwd
ls -l
cd ..

# Работа с файлами
echo "--- File operations ---"
cat documents/README.txt
echo "Reversed README:"
rev documents/README.txt
stat documents/README.txt

# Поиск файлов
echo "--- File search ---"
find / -name "*.txt"
find . -name "*.py" -type f
find . -name "documents" -type d

# Создание файлов (Stage 5)
echo "--- File creation ---"
touch test_file1.txt
touch /tmp/test_file2.txt
ls -l
find . -name "test_file*"

# Древовидная структура
echo "--- Directory tree ---"
tree /home

# Обработка ошибок
echo "--- Error handling ---"
ls /nonexistent_directory
cat nonexistent_file.txt
rev documents/  # Попытка перевернуть директорию
touch /invalid/path/file.txt
find /invalid -name "test"

# Возврат и финальный просмотр
cd /home/user
pwd
ls -l

echo "=== COMPREHENSIVE TEST COMPLETED ==="
