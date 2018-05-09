import io
import tempfile
import os
import mimetypes

from PIL import Image

from django.conf import settings
from django.db import models
from django.template.defaultfilters import slugify, truncatechars
from django.utils import timezone as datetime
from django.utils.html import escape
from django.core.files.uploadedfile import InMemoryUploadedFile, SimpleUploadedFile

from django_countries.fields import CountryField

from separatedvaluesfield.models import SeparatedValuesField

import vimeo

from .project import Project
from .tag import Tag
from .geo import City

# try:
#     from moviepy.editor import ImageClip, AudioFileClip
# except:
#     import imageio
#     imageio.plugins.ffmpeg.download()
#     from moviepy.editor import ImageClip, AudioFileClip


def get_filename(filename):
    fname, ext = os.path.splitext(filename)

    return str('%s%s' % (slugify(truncatechars(fname, 50)), escape(ext)))


VIDEO_FILE_EXTENSION = (
'.264', '.3g2', '.3gp', '.3gp2', '.3gpp', '.3gpp2', '.3mm', '.3p2', '.60d', '.787', '.89', '.aaf', '.aec', '.aep', '.aepx',
'.aet', '.aetx', '.ajp', '.ale', '.am', '.amc', '.amv', '.amx', '.anim', '.aqt', '.arcut', '.arf', '.asf', '.asx', '.avb',
'.avc', '.avd', '.avi', '.avp', '.avs', '.avs', '.avv', '.axm', '.bdm', '.bdmv', '.bdt2', '.bdt3', '.bik', '.bin', '.bix',
'.bmk', '.bnp', '.box', '.bs4', '.bsf', '.bvr', '.byu', '.camproj', '.camrec', '.camv', '.ced', '.cel', '.cine', '.cip',
'.clpi', '.cmmp', '.cmmtpl', '.cmproj', '.cmrec', '.cpi', '.cst', '.cvc', '.cx3', '.d2v', '.d3v', '.dat', '.dav', '.dce',
'.dck', '.dcr', '.dcr', '.ddat', '.dif', '.dir', '.divx', '.dlx', '.dmb', '.dmsd', '.dmsd3d', '.dmsm', '.dmsm3d', '.dmss',
'.dmx', '.dnc', '.dpa', '.dpg', '.dream', '.dsy', '.dv', '.dv-avi', '.dv4', '.dvdmedia', '.dvr', '.dvr-ms', '.dvx', '.dxr',
'.dzm', '.dzp', '.dzt', '.edl', '.evo', '.eye', '.ezt', '.f4p', '.f4v', '.fbr', '.fbr', '.fbz', '.fcp', '.fcproject',
'.ffd', '.flc', '.flh', '.fli', '.flv', '.flx', '.gfp', '.gl', '.gom', '.grasp', '.gts', '.gvi', '.gvp', '.h264', '.hdmov',
'.hkm', '.ifo', '.imovieproj', '.imovieproject', '.ircp', '.irf', '.ism', '.ismc', '.ismv', '.iva', '.ivf', '.ivr', '.ivs',
'.izz', '.izzy', '.jss', '.jts', '.jtv', '.k3g', '.kmv', '.ktn', '.lrec', '.lsf', '.lsx', '.m15', '.m1pg', '.m1v', '.m21',
'.m21', '.m2a', '.m2p', '.m2t', '.m2ts', '.m2v', '.m4e', '.m4u', '.m4v', '.m75', '.mani', '.meta', '.mgv', '.mj2', '.mjp',
'.mjpg', '.mk3d', '.mkv', '.mmv', '.mnv', '.mob', '.mod', '.modd', '.moff', '.moi', '.moov', '.mov', '.movie', '.mp21',
'.mp21', '.mp2v', '.mp4', '.mp4v', '.mpe', '.mpeg', '.mpeg1', '.mpeg4', '.mpf', '.mpg', '.mpg2', '.mpgindex', '.mpl',
'.mpl', '.mpls', '.mpsub', '.mpv', '.mpv2', '.mqv', '.msdvd', '.mse', '.msh', '.mswmm', '.mts', '.mtv', '.mvb', '.mvc',
'.mvd', '.mve', '.mvex', '.mvp', '.mvp', '.mvy', '.mxf', '.mxv', '.mys', '.ncor', '.nsv', '.nut', '.nuv', '.nvc', '.ogm',
'.ogv', '.ogx', '.osp', '.otrkey', '.pac', '.par', '.pds', '.pgi', '.photoshow', '.piv', '.pjs', '.playlist', '.plproj',
'.pmf', '.pmv', '.pns', '.ppj', '.prel', '.pro', '.prproj', '.prtl', '.psb', '.psh', '.pssd', '.pva', '.pvr', '.pxv',
'.qt', '.qtch', '.qtindex', '.qtl', '.qtm', '.qtz', '.r3d', '.rcd', '.rcproject', '.rdb', '.rec', '.rm', '.rmd', '.rmd',
'.rmp', '.rms', '.rmv', '.rmvb', '.roq', '.rp', '.rsx', '.rts', '.rts', '.rum', '.rv', '.rvid', '.rvl', '.sbk', '.sbt',
'.scc', '.scm', '.scm', '.scn', '.screenflow', '.sec', '.sedprj', '.seq', '.sfd', '.sfvidcap', '.siv', '.smi', '.smi',
'.smil', '.smk', '.sml', '.smv', '.spl', '.sqz', '.srt', '.ssf', '.ssm', '.stl', '.str', '.stx', '.svi', '.swf', '.swi',
'.swt', '.tda3mt', '.tdx', '.thp', '.tivo', '.tix', '.tod', '.tp', '.tp0', '.tpd', '.tpr', '.trp', '.ts', '.tsp', '.ttxt',
'.tvs', '.usf', '.usm', '.vc1', '.vcpf', '.vcr', '.vcv', '.vdo', '.vdr', '.vdx', '.veg','.vem', '.vep', '.vf', '.vft',
'.vfw', '.vfz', '.vgz', '.vid', '.video', '.viewlet', '.viv', '.vivo', '.vlab', '.vob', '.vp3', '.vp6', '.vp7', '.vpj',
'.vro', '.vs4', '.vse', '.vsp', '.w32', '.wcp', '.webm', '.wlmp', '.wm', '.wmd', '.wmmp', '.wmv', '.wmx', '.wot', '.wp3',
'.wpl', '.wtv', '.wve', '.wvx', '.xej', '.xel', '.xesc', '.xfl', '.xlmv', '.xmv', '.xvid', '.y4m', '.yog', '.yuv', '.zeg',
'.zm1', '.zm2', '.zm3', '.zmv'  )


def get_image_path(instance, filename):
    if instance.project_id:
        return os.path.join(instance.project.get_media_path(), 'images', get_filename(filename))
    return os.path.join('other', 'images', get_filename(filename))


def get_video_path(instance, filename):
    if instance.project_id:
        if instance.type == instance.AUDIO:
            return os.path.join(instance.project.get_media_path(), 'audios', 'videos', get_filename(filename))
        return os.path.join(instance.project.get_media_path(), 'videos', get_filename(filename))
    return os.path.join('other', 'videos', get_filename(filename))


def get_audio_path(instance, filename):
    if instance.project_id:
        return os.path.join(instance.project.get_media_path(), 'audios', get_filename(filename))
    return os.path.join('other', 'audios', get_filename(filename))


class Media(models.Model):
    IMAGE = 0
    VIDEO = 1
    AUDIO = 2
    TYPE_CHOICES = (
        (IMAGE, 'Image'),
        (VIDEO, 'Video'),
        (AUDIO, 'Audio'),
    )
    type = models.IntegerField(choices=TYPE_CHOICES)
    title = models.CharField(max_length=255, null=True, blank=True)
    project = models.ForeignKey(Project, null=True, related_name='medias')
    created_at = models.DateTimeField(default=datetime.now)
    realized_at = models.DateTimeField(null=True)
    country = CountryField(null=True)
    city = models.ForeignKey(City, null=True)
    position = models.PositiveIntegerField(null=True)

    image = models.ImageField(upload_to=get_image_path,
                              blank=True,
                              null=True)

    video = models.FileField(upload_to=get_video_path, null=True, blank=True)

    audio = models.FileField(upload_to=get_audio_path, null=True, blank=True)

    thumbnail_file = models.ImageField(upload_to=get_image_path,
                                       blank=True,
                                       null=True)
    languages = SeparatedValuesField(max_length=255,
                                     blank=True,
                                     null=True)

    url = models.URLField(blank=True, null=True)

    tags = models.ManyToManyField(Tag)

    def next_media(self):
        default = Media.objects.filter(project=self.project, id__gt=self.id).first()
        return Media.objects.filter(project=self.project, position=self.position+1).first() if self.position else default or default

    def is_video_file(self):
        return self.video.name.endswith(VIDEO_FILE_EXTENSION)

    def upload_to_vimeo(self):
        if not self.video.name or not hasattr(settings, 'VIMEO_CLIENT_ID'):
            return

        v = vimeo.VimeoClient(token=settings.VIMEO_CLIENT_TOKEN,
                              key=settings.VIMEO_CLIENT_ID,
                              secret=settings.VIMEO_CLIENT_SECRET)

        vimeo_account_data = v.get('/me').json()

        if self.video.file.size > vimeo_account_data['upload_quota']['space']['free']:
            # TODO send email to zim and I
            return

        data = {
                'type' : 'pull',
                'link' : self.video.url
        }

        response = v.post('/me/videos', data=data).json()
        self.url = response.get('link')
        self.save()
        self.edit_vimeo_information()

    def edit_vimeo_information(self, change_thumbnail=False):
        if not self.url or not hasattr(settings, 'VIMEO_CLIENT_ID'):
            return

        video_uri = self.url.split('https://vimeo.com/')
        if len(video_uri) != 2:
            return

        video_uri = '/videos/%s' % video_uri[1]

        v = vimeo.VimeoClient(token=settings.VIMEO_CLIENT_TOKEN,
                              key=settings.VIMEO_CLIENT_ID,
                              secret=settings.VIMEO_CLIENT_SECRET)

        v.patch(video_uri, data={'name': self.title_en})
        v.put('%s/tags' % video_uri, data=[{'tag': tag.name_en} for tag in self.tags.all()])

        if self.thumbnail_file and change_thumbnail:
            with tempfile.NamedTemporaryFile() as temp:
                temp.write(self.thumbnail_file.file.read())
                v.upload_picture(video_uri, temp.name, activate=True)

    def transform_audio_to_video(self):
        # if (self.type != self.AUDIO
        #     or not self.audio
        #     or not self.thumbnail_file):
        #     return None

        # audio_split = self.audio.url.split('/')
        # audio_file_name = audio_split[len(audio_split) - 1]
        # audio_name = audio_file_name.split('.')[0]

        # image_clip = ImageClip(self.thumbnail_file.url)
        # audio_clip = AudioFileClip(self.audio.url)

        # clip = image_clip.set_audio(audio_clip)
        # clip = clip.set_duration(audio_clip.duration)

        # with tempfile.NamedTemporaryFile(suffix='%s.mp4' % audio_name) as temp:
        #     clip.write_videofile(temp.name, fps=1)
        #     self.video = SimpleUploadedFile('%s.mp4' % audio_name, temp.file.read(), content_type='video/mp4')
        #     self.save()
        #     self.upload_to_vimeo()
        pass

    class Meta:
        abstract = False
        db_table = 'mnemotopy_project_media'
