# Fastapi-Template

### Build FastAPI Services
```
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### Code generate relative

DB-First
```
sqlacodegen --outfile models.py mysql+pymysql://root@localhost:3306/{DB_NAME}
```

### SQL Relative

刪除某個 Table 所有資料
```
-- 暫時禁用安全模式
SET SQL_SAFE_UPDATES = 0;

-- 刪除所有資料
DELETE FROM sample_table;

-- 再次啟用安全模式
SET SQL_SAFE_UPDATES = 1;
```

### Docker Relative

建立 Docker 
```
docker-compose up --build
docker-compose up --build -d
docker-compose down && docker-compose up --build
```

重啟某個 Docker 服務
```
docker-compose restart app
```

列出來永久保存的 Docker 資源
```
docker volume ls

DRIVER    VOLUME NAME
local     example_db_data
```

Check Docker logs
```
docker-compose logs
```

Check 運行中的 Docker
```
docker-compose ps

CONTAINER ID   IMAGE          COMMAND                   CREATED              STATUS              PORTS                    NAMES
ddb1760a05f7   example-app   "uvicorn app.main:ap…"   About a minute ago   Up About a minute   0.0.0.0:8000->8000/tcp    **example-app**
8c0d489062cb   mariadb:10.5   "docker-entrypoint.s…"   About a minute ago   Up About a minute   0.0.0.0:3306->3306/tcp   example-db
```

進入 example-app 中
```
docker exec -it example-app /bin/bash
```

進入 example-db 中，帳號密碼會跟 .env 相同
```
docker exec -it example-db mysql -u example_user -p

進入之後：
USE example_db;
SHOW TABLES;
DESC table_name;
```

### AWS Relative

連線到 AWS (with password)
```
ssh ec2-user@{AWS_IP_ADDRESS)
```

第一次要先更新 yum (AWS 是用 yum，而不是用 apt)
```
sudo yum update -y
sudo yum upgrade -y
```

安裝 docker
```
sudo yum install -y docker
sudo yum install -y git
```

安裝 docker-compose
```
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
```

更改 docker-compose 權限
```
sudo chmod +x /usr/local/bin/docker-compose
```

### Others

取的當前目錄下的資料夾結構，可以再丟給 gpt 
```
# 遍歷當前資料夾結構，列出所有檔案和目錄
Get-ChildItem -Recurse | Format-Table -Property FullName
```


