BEGIN;

CREATE TABLE IF NOT EXISTS cities_city (
id serial NOT NULL PRIMARY KEY,
name varchar(200) NOT NULL,
slug varchar(200) NOT NULL,
country varchar(2) NULL);

CREATE TABLE IF NOT EXISTS mnemotopy_project (
id serial NOT NULL PRIMARY KEY,
slug varchar(50) NOT NULL,
name varchar(255) NULL,
subtitle varchar(255) NULL,
description text NULL, created_at timestamp with time zone NOT NULL,
started_at timestamp with time zone NULL,
ended_at timestamp with time zone NULL,
country varchar(2) NULL,
archived boolean NOT NULL,
position integer NULL CHECK (position >= 0),
published boolean NOT NULL,
city_id integer REFERENCES cities_city (id) DEFERRABLE INITIALLY DEFERRED);

CREATE TABLE IF NOT EXISTS mnemotopy_projectslug (
id serial NOT NULL PRIMARY KEY,
object_id integer NOT NULL CHECK (object_id >= 0),
slug varchar(255) NOT NULL UNIQUE,
redirect boolean NOT NULL,
created timestamp with time zone NOT NULL,
content_type_id integer NOT NULL REFERENCES django_content_type (id) DEFERRABLE INITIALLY DEFERRED);

CREATE TABLE IF NOT EXISTS mnemotopy_category (
id serial NOT NULL PRIMARY KEY,
name varchar(255) NULL,
description text NULL,
created_at timestamp with time zone NOT NULL,
slug varchar(50) NOT NULL);

CREATE TABLE IF NOT EXISTS mnemotopy_project_categories (
id serial NOT NULL PRIMARY KEY,
project_id integer NOT NULL REFERENCES mnemotopy_project (id) DEFERRABLE INITIALLY DEFERRED,
category_id integer NOT NULL REFERENCES mnemotopy_category (id) DEFERRABLE INITIALLY DEFERRED,
UNIQUE (project_id, category_id));

CREATE TABLE IF NOT EXISTS mnemotopy_tag (
id serial NOT NULL PRIMARY KEY,
name varchar(255) NULL,
slug varchar(50) NOT NULL,
created_at timestamp with time zone NOT NULL);

CREATE TABLE IF NOT EXISTS mnemotopy_project_tags (
id serial NOT NULL PRIMARY KEY,
project_id integer NOT NULL REFERENCES mnemotopy_project (id) DEFERRABLE INITIALLY DEFERRED,
tag_id integer NOT NULL REFERENCES mnemotopy_tag (id) DEFERRABLE INITIALLY DEFERRED,
UNIQUE (project_id, tag_id));


CREATE TABLE IF NOT EXISTS mnemotopy_project_image (
id serial NOT NULL PRIMARY KEY,
title varchar(255) NULL,
created_at timestamp with time zone NOT NULL,
realized_at timestamp with time zone NULL,
country varchar(2) NULL,
position integer NULL CHECK (position >= 0),
image varchar(100) NULL,
city_id integer REFERENCES cities_city (id) DEFERRABLE INITIALLY DEFERRED,
project_id integer REFERENCES mnemotopy_project (id) DEFERRABLE INITIALLY DEFERRED);

CREATE TABLE IF NOT EXISTS mnemotopy_project_audio (
id serial NOT NULL PRIMARY KEY,
title varchar(255) NULL,
created_at timestamp with time zone NOT NULL,
realized_at timestamp with time zone NULL,
country varchar(2) NULL,
position integer NULL CHECK (position >= 0),
url varchar(200) NULL,
file varchar(100) NULL,
languages varchar(255) NULL,
city_id integer REFERENCES cities_city (id) DEFERRABLE INITIALLY DEFERRED,
project_id integer REFERENCES mnemotopy_project (id) DEFERRABLE INITIALLY DEFERRED);

CREATE TABLE IF NOT EXISTS mnemotopy_project_video (
id serial NOT NULL PRIMARY KEY,
title varchar(255) NULL,
created_at timestamp with time zone NOT NULL,
realized_at timestamp with time zone NULL,
country varchar(2) NULL,
position integer NULL CHECK (position >= 0),
url varchar(200) NULL,
file varchar(100) NULL,
languages varchar(255) NULL,
city_id integer REFERENCES cities_city (id) DEFERRABLE INITIALLY DEFERRED,
project_id integer REFERENCES mnemotopy_project (id) DEFERRABLE INITIALLY DEFERRED);


CREATE INDEX IF NOT EXISTS cities_city_b068931c ON cities_city (name);

CREATE INDEX IF NOT EXISTS mnemotopy_project_image_c7141997 ON mnemotopy_project_image (city_id);

CREATE INDEX IF NOT EXISTS mnemotopy_project_c7141997 ON mnemotopy_project (city_id);

CREATE INDEX IF NOT EXISTS mnemotopy_project_categories_b098ad43 ON mnemotopy_project_categories (project_id);

CREATE INDEX IF NOT EXISTS mnemotopy_project_categories_b583a629 ON mnemotopy_project_categories (category_id);

 CREATE INDEX IF NOT EXISTS mnemotopy_project_video_c7141997 ON mnemotopy_project_video (city_id);

 CREATE INDEX IF NOT EXISTS mnemotopy_project_video_b098ad43 ON mnemotopy_project_video (project_id);

 CREATE INDEX IF NOT EXISTS mnemotopy_project_tags_b098ad43 ON mnemotopy_project_tags (project_id);

 CREATE INDEX IF NOT EXISTS mnemotopy_project_tags_76f094bc ON mnemotopy_project_tags (tag_id);

 CREATE INDEX IF NOT EXISTS mnemotopy_project_image_b098ad43 ON mnemotopy_project_image (project_id);

CREATE INDEX IF NOT EXISTS mnemotopy_project_audio_c7141997 ON mnemotopy_project_audio (city_id);

CREATE INDEX IF NOT EXISTS mnemotopy_project_audio_b098ad43 ON mnemotopy_project_audio (project_id);

CREATE INDEX IF NOT EXISTS mnemotopy_category_2dbcba41 ON mnemotopy_category (slug);

CREATE INDEX IF NOT EXISTS mnemotopy_category_slug_3083a450_like ON mnemotopy_category (slug varchar_pattern_ops);

CREATE INDEX IF NOT EXISTS mnemotopy_project_2dbcba41 ON mnemotopy_project (slug);

CREATE INDEX IF NOT EXISTS mnemotopy_project_slug_c7622499_like ON mnemotopy_project (slug varchar_pattern_ops);

CREATE INDEX IF NOT EXISTS mnemotopy_projectslug_417f1b1c ON mnemotopy_projectslug (content_type_id);

CREATE INDEX IF NOT EXISTS mnemotopy_projectslug_slug_82b03612_like ON mnemotopy_projectslug (slug varchar_pattern_ops);

CREATE INDEX IF NOT EXISTS mnemotopy_tag_2dbcba41 ON mnemotopy_tag (slug);

CREATE INDEX IF NOT EXISTS mnemotopy_tag_slug_a6f0d824_like ON mnemotopy_tag (slug varchar_pattern_ops);

COMMIT;
