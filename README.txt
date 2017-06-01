Website for Mnemotopy project


=====
TODOs
=====

Switch from french to english easily - done

Login view - ok

Admin to create categories, tags, users

------------------------------
Form/View to create an article
------------------------------

- Add text (with videos and audios)
- Add images with an order and a default image for the project
- Set categories to project
- Set keywords to project
- Possibility to set a position (to up in list)
- Archive (not in main list)
- Publish article (if ready)


--------------------------------
View to display list of projects
--------------------------------

- Waiting for design
- Display only un-archived articles for the selected category/ies


------------------------
View to display archives
------------------------

- Possibility to search in projects (fulltext search)
- Wait for list of filters availables


----
Home
----

- Waiting for design
- Enter in website by categories


----------
Media form
----------

TODO:
- On media video upload, celery task to send to vimeo


----------
Backoffice
----------

- Css
- Menu with "back to list" and "see my project"



----
URLS
----

Edit
- edit/projects : list of projects to edit - paginated
- edit/projects/add: create project
- edit/projects/id: edit main information on project
- edit/projects/id/medias: edit medias on project
- edit/projects/id/medias/add: add media to project (get -> html form)
- edit/projects/id/medias/id/: edit media of a project (get -> html form)
- edit/projects/id/medias/id/delete: delete media
- /admin
- /login
- /logout


Public views
- / : home - choose between categories (?)
- /category1/category2: list project matching category-ies chosen, archived not in list (all must be an option)
- /projects/slug : detail project
- /projects/slug/medias/id: slideshow, paginated, called with ajax to avoid changing url, if no id, redirect to first
- /change_language: change language post view
- /archive: list of all projects


------------------
Design BO - prio 2
------------------
- design country list - prio 2 (if there is some time)
- Drag drop file - prio 2 (nice to have)

----
Bugs
----

- display empty instead of default english when no french... FIXED


TODO:
- Faire page tri par categorie + Paginated
- Faire le slideshow avec la gestion ajax du next/previous
- SEO
- Google analytics

- Prendre un vps pour le serveur


-----
VIMEO
-----

- On video upload, if file type in indead video media.upload_to_vimeo()
- media.upload_to_vimeo -> if settings vimeo are set, upload to vimeo in celery task
- upload_vimeo: check if space left, if no space left, sends mail to stephan and I "the video link on project link has not been uploaded to vimeo due to lack of space", else upload to vimeo



------
SERVOR
------

- Install postgres
- Create db + user
- migrate

- Install rabbitmq
- Create user + vhost

- Clone code and install requirements

- Create vimeo pro account for stephan

- edit prod settings

- launch servor http://techstream.org/Web-Development/Deploy-Django-Project

- start queues

- DNS configuration
