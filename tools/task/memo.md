```sql
CREATE TABLE Users (
    UserID INT PRIMARY KEY,
    Username VARCHAR(255) NOT NULL,
    Password VARCHAR(255) NOT NULL,
    AccountCreationDate DATETIME NOT NULL
);

-- タスクテーブル
CREATE TABLE Tasks (
    TaskID INT PRIMARY KEY,
    UserID INT,
    TaskContent TEXT NOT NULL,
    Priority VARCHAR(50) NOT NULL,
    DueDate DATE NOT NULL,
    Progress INT,
    FOREIGN KEY (UserID) REFERENCES Users(UserID)
);

-- プロジェクトテーブル
CREATE TABLE Projects (
    ProjectID INT PRIMARY KEY,
    UserID INT,
    ProjectName VARCHAR(255) NOT NULL,
    FOREIGN KEY (UserID) REFERENCES Users(UserID)
);
```

npm i -g @nestjs/cli