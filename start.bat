@echo off
echo =====================================
echo ��������ǰ�����Ŀ��Windows��
echo =====================================

REM ����ǰ��
cd frontend
echo ���ڰ�װǰ������...
call npm install

echo ����ǰ�˷����У�npm run dev��...
start cmd /k "npm run dev"

cd ..
cd backend

echo ������˷����У�python app.py��...
start cmd /k "python app.py"

echo ���з���������������������з���http://localhost:5173/RedMansions��