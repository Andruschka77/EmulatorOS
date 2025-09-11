# Stage 4 Test Script - Basic Commands
echo "=== STAGE 4 TEST: BASIC COMMANDS ==="

# ������������ ����������� ls
echo "--- Testing ls command ---"
ls
ls -l
ls /home
ls -la /home/user

# ������������ ����������� cd
echo "--- Testing cd command ---"
pwd
cd documents
pwd
cd ..
pwd
cd /etc
pwd
cd /home/user

# ������������ rev
echo "--- Testing rev command ---"
cat documents/README.txt
echo "Reversed:"
rev documents/README.txt

# ������������ find
echo "--- Testing find command ---"
find / -name "*.txt"
find /home -name "*.py" -type f
find . -name "music" -type d

# ��������� ������
echo "--- Error handling ---"
ls /nonexistent
rev nonexistent_file.txt
find /invalid -name "test"
cd /invalid/path

echo "=== STAGE 4 TEST COMPLETED ==="
