#! /bin/bash

# 删除原数据
sudo rm -r ./mysql/data/
sudo rm -r ./web/source/
sudo rm -r ./nginx/log/
sudo cp -r ../api_todo/ ./web/source/

# 复制requirement.txt 和 项目文件
cd ..
sudo chmod -R 777 deployment/
. venv/bin/activate
cd deployment/web/
pip freeze > requirements.txt
deactivate
