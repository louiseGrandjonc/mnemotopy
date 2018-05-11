from mnemotopy.models import Media
from mnemotopy.utils.queryset import queryset_to_dict

def preload_projects_main_image(projects):
    query = '''SELECT DISTINCT ON (project_id) id, project_id, position, created_at, type, title_en, title_fr, country, image, video, audio, thumbnail_file, languages, url, city_id, project_id FROM mnemotopy_project_media WHERE project_id IN %s AND (image IS NOT NULL OR thumbnail_file IS NOT NULL) GROUP BY (project_id, position, created_at, id) ORDER BY project_id DESC, COALESCE(position, 2) ASC, created_at DESC'''

    medias = queryset_to_dict(Media.objects.raw(query, params=[tuple([p.id for p in projects])]), key='project_id')

    for p in projects:
        media = medias.get(p.pk)
        setattr(p, 'main_media', media)

    return projects
