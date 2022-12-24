DROP TABLE IF EXISTS UID_TABLE;
CREATE TABLE UID_TABLE(
    user_id VARCHAR(64) NOT NULL   COMMENT '用户ID' ,
    uid VARCHAR(32) NOT NULL   COMMENT '游戏UID' ,
    update_time DATETIME NOT NULL   COMMENT '上次更新时间' ,
    PRIMARY KEY (user_id)
)  COMMENT = 'UID数据库';