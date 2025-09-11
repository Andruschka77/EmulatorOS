# Comprehensive Test Script for All Stages
echo "=== COMPREHENSIVE VFS TERMINAL TEST ==="

# �������� ���������� � VFS
vfs_info

# ��������� � ��������
pwd
ls -l
cd documents
pwd
ls -l
cd ..

# ������ � �������
echo "--- File operations ---"
cat documents/README.txt
echo "Reversed README:"
rev documents/README.txt
stat documents/README.txt

# ����� ������
echo "--- File search ---"
find / -name "*.txt"
find . -name "*.py" -type f
find . -name "documents" -type d

# �������� ������ (Stage 5)
echo "--- File creation ---"
touch test_file1.txt
touch /tmp/test_file2.txt
ls -l
find . -name "test_file*"

# ����������� ���������
echo "--- Directory tree ---"
tree /home

# ��������� ������
echo "--- Error handling ---"
ls /nonexistent_directory
cat nonexistent_file.txt
rev documents/  # ������� ����������� ����������
touch /invalid/path/file.txt
find /invalid -name "test"

# ������� � ��������� ��������
cd /home/user
pwd
ls -l

echo "=== COMPREHENSIVE TEST COMPLETED ==="
