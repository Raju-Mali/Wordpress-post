CREATE TABLE IF NOT EXISTS post (
    post_id INTEGER PRIMARY KEY AUTOINCREMENT,
    post_title TEXT,
    post_blog_post TEXT,
    post_blog_extra TEXT,
    post_excerpt TEXT,
    post_category TEXT,
    post_pub_date TEXT,
    post_create_date TEXT,
    post_mod_date TEXT,
    post_tag_id INTEGER
);

CREATE TABLE IF NOT EXISTS hash (
    hash_id INTEGER PRIMARY KEY AUTOINCREMENT,
    hash_label TEXT,
    hash_post_id INTEGER,
    FOREIGN KEY (hash_post_id) REFERENCES post (post_tag_id)
);

