





/*
 生成基础测试数据表
*/


CREATE TABLE IF NOT EXISTS v_t (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    address VARCHAR(255),
    email VARCHAR(100),
    phone_number VARCHAR(30),
    birthdate DATE
);


/*
在基础表的数据基础上，复制一个新表
*/

CREATE TABLE v_t1 LIKE v_t;
INSERT INTO v_t1 SELECT * FROM v_t;


SELECT
    (SELECT COUNT(*) FROM v_t) AS count_v_t,
    (SELECT COUNT(*) FROM v_t1) AS count_v_t1,
    (SELECT COUNT(*)
     FROM v_t
     WHERE (id, name, address, email, phone_number, birthdate) NOT IN
           (SELECT id, name, address, email, phone_number, birthdate FROM v_t1)
    ) AS mismatch_count;


/*
如果数据表有30个字段，如何批量比较

下面整体比较是有效的

*/




-- 第一个是查询不同表的结果对比，

select *

from (
    select * from v_t
    union
    select * from v_t1
) as combined

group by id having count(*) > 1;



-- 第二个是查询一个表中，同一字段的不同查询条件进行的对比

SELECT *
FROM (
    (SELECT id, name, address, email, phone_number, birthdate
FROM v_t
WHERE id=22)
    UNION all
    (SELECT id, name, address, email, phone_number, birthdate
FROM v_t
WHERE id=23)
) AS combined
group by id having count(*)=count(*);

(SELECT id, name, address, email, phone_number, birthdate FROM v_t WHERE id=22)
和
(SELECT id, name, address, email, phone_number, birthdate FROM v_t WHERE id=23)
比较上面的SQL结果，按照id, name, address, email, phone_number, birthdate进行遍历比较，如果同一个字段名的数据相同，则什么都不处理，如果出现差异就只输出差异的字段结果即可

2024/7/14 17:43:17



-- 抓住通性，只比较一个字段的的2个结果，遍历

-- Update email for IDs 16 and 17 to an empty string
UPDATE v_t SET email = '0' WHERE id IN (16, 17);

-- Update address for ID 18 to two double quotes
UPDATE v_t SET address = '0' WHERE id = 18;


-- 联合


SELECT
    CASE WHEN t1.name != t2.name THEN 'name' ELSE NULL END AS name_diff,
    CASE WHEN t1.address != t2.address THEN 'address' ELSE NULL END AS address_diff,
    CASE WHEN t1.email != t2.email THEN 'email' ELSE NULL END AS email_diff,
    CASE WHEN t1.phone_number != t2.phone_number THEN 'phone_number' ELSE NULL END AS phone_number_diff,
    CASE WHEN t1.birthdate != t2.birthdate THEN 'birthdate' ELSE NULL END AS birthdate_diff
FROM
    vt t1
JOIN
    table2 t2 ON t1.id = 22 AND t2.id = 23
WHERE
    t1.id = 22 AND t2.id = 23
    AND (
        t1.name != t2.name OR
        t1.address != t2.address OR
        t1.email != t2.email OR
        t1.phone_number != t2.phone_number OR
        t1.birthdate != t2.birthdate
    );

-- 查詢一個字段的結果 ok
WITH tmp1 AS (
    SELECT id, name, address, email, phone_number, birthdate
    FROM v_t
    WHERE id in (12,13,14)
),
tmp2 AS (
    SELECT id, name, address, email, phone_number, birthdate
    FROM v_t
    WHERE id in (22,23,24)
)
SELECT
    CASE WHEN tmp1.email = tmp2.email  THEN 'ok' ELSE 'failed' END AS email_diff

FROM
    tmp1,tmp2;


上面的sql得到了下面的结果上面的
结果，null有2次，low有一次，但是有修改后的代码无法查询到






+------------+
| email_diff |
+------------+
| ok         |
| failed     |
| ok         |
+------------+

优化SQL的需求
再针对于 email_diff 进行计数分类 ，如果是 Low,就接设置为email_diff_low,然后计数；如果是NULL，就接设置为email_diff_null,然后计数


WITH tmp1 AS (
    SELECT id, name, address, email, phone_number, birthdate
    FROM v_t
    WHERE id IN (12, 13, 14)
),
tmp2 AS (
    SELECT id, name, address, email, phone_number, birthdate
    FROM v_t
    WHERE id IN (22, 23, 24)
)
SELECT
    SUM(CASE WHEN email_diff = 'ok' THEN 1 ELSE 0 END) AS email_diff_ok
    SUM(CASE WHEN email_diff = 'failed'  THEN 1 ELSE 0 END) AS email_diff_failed
FROM (
    SELECT
       CASE WHEN tmp1.email = tmp2.email  THEN 'ok' ELSE 'failed' END AS email_diff
    FROM
        tmp1
    JOIN
        tmp2 ON tmp1.id = tmp2.id
) AS diff_analysis;














WITH tmp1 AS (
    SELECT id, name, address, email, phone_number, birthdate
    FROM v_t
    WHERE id IN (12, 13, 14)
),
tmp2 AS (
    SELECT id, name, address, email, phone_number, birthdate
    FROM v_t
    WHERE id IN (22, 23, 24)
),
diff_analysis AS (
    SELECT
        CASE WHEN tmp1.email = tmp2.email THEN 'ok' ELSE 'failed' END AS email_diff
    FROM
        tmp1，tmp2
)
SELECT
    SUM(CASE WHEN email_diff = 'ok' THEN 1 ELSE 0 END) AS email_diff_ok,
    SUM(CASE WHEN email_diff = 'failed' THEN 1 ELSE 0 END) AS email_diff_failed
FROM
    diff_analysis;



-- SQL2 解决了批量判断为零的问题   这个用来统计一个数据表的两个查询条件的，为零的情况是比较方面
   WITH tmp1 AS (
    SELECT id, name, address, email, phone_number, birthdate
    FROM v_t
    WHERE id IN (14, 15,16)
),
tmp2 AS (
    SELECT id, name, address, email, phone_number, birthdate
    FROM v_t
    WHERE id IN (22, 23, 24)
),
emails AS (
    SELECT email FROM tmp1
    UNION
    SELECT email FROM tmp2
)
SELECT email,
       COUNT(CASE WHEN in_tmp1 THEN 1 ELSE 0 END) AS in_tmp1_count,
       COUNT(CASE WHEN in_tmp2 THEN 1 ELSE 0 END) AS in_tmp2_count
FROM (
    SELECT email, TRUE AS in_tmp1, FALSE AS in_tmp2 FROM tmp1
    UNION ALL
    SELECT email, FALSE AS in_tmp1, TRUE AS in_tmp2 FROM tmp2
) AS combined_emails
GROUP BY email;


-- 整体进行查询比较还是直接用新的数据进行导出整理吧 然后再去一个一个比较，因为还涉及到了排序的问题，没有上面的结果来的简写
--这对上面两个临时表，想要进行排序整理，比如id的话就分别形成 tmp1_id,tmp2_id 并排整理，后面的字段都以此类推
--最终输出新的数据表 直接导出测试的结果，省的说作假啥的


-- c
   WITH tmp1 AS (
    SELECT id, name, address, email, phone_number, birthdate
    FROM v_t
    WHERE id IN (14, 15,16)
),
tmp2 AS (
    SELECT id, name, address, email, phone_number, birthdate
    FROM v_t
    WHERE id IN (22, 23, 24)
)

select tmp1.id,tmp2.id,tmp1.email as tmp1_id,tmp2.email as tmp2_id,
    CASE WHEN tmp1.email = tmp2.email  THEN 'ok' ELSE 'failed' END AS id_diff

 from tmp1,tmp2;


   WITH tmp1 AS (
    SELECT id, name, address, email, phone_number, birthdate
    FROM v_t
    WHERE id IN (14, 15,16)
),
tmp2 AS (
    SELECT id, name, address, email, phone_number, birthdate
    FROM v_t
    WHERE id IN (22, 23, 24)
)



WITH tmp1 AS (
    SELECT id, name, address, email, phone_number, birthdate,
           ROW_NUMBER() OVER () AS rn
    FROM v_t
    WHERE id IN (14, 15, 16)
),
tmp2 AS (
    SELECT id, name, address, email, phone_number, birthdate,
           ROW_NUMBER() OVER () AS rn
    FROM v_t
    WHERE id IN (22, 23, 24)
)

-- 将 tmp1 和 tmp2 的查询结果合并并分别展示在不同列
SELECT tmp1.id AS tmp1_id, tmp2.id AS tmp2_id
FROM tmp1
UNION tmp2
ON tmp1.rn = tmp2.rn;


--- 整体横向展示 基本可以用

WITH tmp1 AS (
    SELECT id, name, address, email, phone_number, birthdate
    FROM v_t
    WHERE id IN (14, 15, 16)
),
tmp2 AS (
    SELECT id, name, address, email, phone_number, birthdate
    FROM v_t
    WHERE id IN (22, 23, 24)
)

-- 将 tmp1 和 tmp2 的查询结果纵向展示，并统计 id 字段
SELECT 'tmp1' AS source, id AS tmp1_id, NULL AS tmp2_id, name, address, email, phone_number, birthdate
FROM tmp1
UNION ALL
SELECT 'tmp2' AS source, NULL AS tmp1_id, id AS tmp2_id, name, address, email, phone_number, birthdate
FROM tmp2;


-- SQL1 用手动逐个导出字段数据， 然后再去逐个比较 用手动一个一个导出再比较吧
WITH tmp1 AS (
    SELECT id, name, address, email, phone_number, birthdate
    FROM v_t
    WHERE id IN (14, 15, 16)
),
tmp2 AS (
    SELECT id, name, address, email, phone_number, birthdate
    FROM v_t
    WHERE id IN (22, 23, 24)
)

-- 将 tmp1 和 tmp2 的查询结果纵向展示，并统计 id 字段


SELECT 'diff' AS diff, 'tmp1_id' AS tmp1_id, 'tmp2_id' AS tmp2_id
UNION ALL
SELECT 'tmp1' AS diff, id AS tmp1_id, NULL AS tmp2_id
FROM tmp1
UNION ALL
SELECT 'tmp2' AS diff, NULL AS tmp1_id, id AS tmp2_id
FROM tmp2
INTO OUTFILE 'C:\\360Downloads\\output_file.csv'
FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n';

-- 导出这个表的所有字段名 下面也是可以的
SELECT COLUMN_NAME
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_SCHEMA = 'vt' AND TABLE_NAME = 'v_t'
INTO OUTFILE 'C:\\360Downloads\\your_output_file.csv'
FIELDS TERMINATED BY ',' ENCLOSED BY '"'
LINES TERMINATED BY '\n';


SELECT COLUMN_NAME
FROM INFORMATION_SCHEMA.COLUMNS
WHERE  TABLE_NAME = 'v_t'
INTO OUTFILE 'C:\\360Downloads\\your_output_file.csv'
FIELDS TERMINATED BY ',' ENCLOSED BY '"'
LINES TERMINATED BY '\n';
