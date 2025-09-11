# Stage 4 Test Script - Basic Commands
echo "=== STAGE 4 TEST: BASIC COMMANDS ==="

# Тестирование улучшенного ls
echo "--- Testing ls command ---"
ls
ls -l
ls /home
ls -la /home/user

# Тестирование улучшенного cd
echo "--- Testing cd command ---"
pwd
cd documents
pwd
cd ..
pwd
cd /etc
pwd
cd /home/user

# Тестирование rev
echo "--- Testing rev command ---"
cat documents/README.txt
echo "Reversed:"
rev documents/README.txt

# Тестирование find
echo "--- Testing find command ---"
find / -name "*.txt"
find /home -name "*.py" -type f
find . -name "music" -type d

# Обработка ошибок
echo "--- Error handling ---"
ls /nonexistent
rev nonexistent_file.txt
find /invalid -name "test"
cd /invalid/path

echo "=== STAGE 4 TEST COMPLETED ==="
