## 更新


### 版本1 to 版本2

#### 数据迁移
##### 1. 迁移文章分类

- 1.0的字段：id、slug、title
- 2.0的字段：id、slug、name、level(设置默认值为1)

```sql
INSERT INTO codelieche.article_category (id, slug, name, level)
SELECT id,slug,title, 1 as 'level' FROM codelieche_1.article_category;
```

##### 2. 迁移文章标签

- 1.0的字段：id、slug、name、hot
- 2.0的字段：id、slug、name、is_hot

```sql
INSERT INTO codelieche.article_tag (id, slug, name, is_hot)
SELECT id,slug,name,hot FROM codelieche_1.article_tag;
```

##### 3. 迁移文章
- 1.0的字段：id,title,content,created,updated,status,top,good,deleted,visit_count,reply_count,author_id,category_id
- 2.0的字段：id, title, content, time_added, time_updated,status,is_top,is_good,deleted,visit_count,reply_count,author_id,category_id

```sql
INSERT INTO codelieche.article_post (id, title, content, time_added, time_updated,status,is_top,is_good,deleted,visit_count,reply_count,author_id,category_id)
SELECT id,title,content,created,updated,status,top,good,deleted,visit_count,reply_count,author_id,category_id FROM codelieche_1.article_post;
```




