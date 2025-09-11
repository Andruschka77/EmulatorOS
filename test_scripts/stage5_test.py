# Stage 5 Test Script - Additional Commands
echo "=== STAGE 5 TEST: ADDITIONAL COMMANDS ==="

# Тестирование touch
echo "--- Testing touch command ---"
ls documents/
touch documents/new_file.txt
touch /home/user/new_file2.txt
ls documents/

# Попытка создания существующего файла
touch documents/README.txt

# Создание файлов в разных директориях
cd /tmp
touch temp_file1 temp_file2
ls
cd /home/user

# Комплексный тест всех команд
echo "--- Comprehensive test ---"
pwd
ls -l
find . -name "new_file*"
cat documents/new_file.txt
stat documents/new_file.txt

# Обработка ошибок touch
echo "--- Error handling for touch ---"
touch /invalid/path/file.txt
touch documents/nonexistent_dir/file.txt

echo "=== STAGE 5 TEST COMPLETED ==="
