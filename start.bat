@echo off
echo =====================================
echo 正在启动前后端项目（Windows）
echo =====================================

REM 启动前端
cd frontend
echo 正在安装前端依赖...
call npm install

echo 启动前端服务中（npm run dev）...
start cmd /k "npm run dev"

cd ..
cd backend

echo 启动后端服务中（python app.py）...
start cmd /k "python app.py"

echo 所有服务已启动，请在浏览器中访问http://localhost:5173/RedMansions。