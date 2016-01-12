from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import re

class Category(models.Model):
    name = models.CharField(max_length=100)
    order = models.IntegerField(default=0)

class Forum(models.Model):
    category = models.ForeignKey(Category)
    name = models.CharField(max_length=200)
    topics = models.PositiveIntegerField(default=0)
    posts = models.PositiveIntegerField(default=0)
    order = models.IntegerField(default=0)
    last_post = models.ForeignKey('Post',  related_name='last_forum_post', null=True, blank=True)
    slug = models.SlugField(null=True, blank=True)
    
    def url(self):
        return "/forum/%s" % self.id

class Topic(models.Model):
    user = models.ForeignKey(User)
    forum = models.ForeignKey('Forum')
    title = models.CharField(max_length=250)
    first_post = models.ForeignKey('Post', related_name='first_topic_post')
    last_post = models.ForeignKey('Post', related_name='last_topic_post')
    views = models.PositiveIntegerField(default=0)
    replies = models.PositiveIntegerField(default=0)
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(null=True, blank=True)
    deleted = models.BooleanField(default=False)
    slug = models.SlugField(null=True, blank=True)
    
    def url(self):
        return "/topic/%s" % self.id

class Post(models.Model):
    forum = models.ForeignKey('Forum')
    topic = models.ForeignKey('Topic')
    user = models.ForeignKey(User)
    ip = models.GenericIPAddressField()
    content = models.TextField()
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(null=True, blank=True)
    deleted = models.BooleanField(default=False)
    
    def url(self):
        return "/post/%s" % self.id
    
    def formatted_content(self):
        formatted_content = self.content
        
        bold_open = re.compile(r'\[b:([a-zA-Z0-9]+)\]', re.IGNORECASE)
        formatted_content = bold_open.sub(r'<b>', formatted_content)
        bold_close = re.compile(r'\[\/b:([a-zA-Z0-9]+)\]', re.IGNORECASE)
        formatted_content = bold_close.sub(r'</b>', formatted_content)
        
        italic_open = re.compile(r'\[i:([a-zA-Z0-9]+)\]', re.IGNORECASE)
        formatted_content = italic_open.sub(r'<i>', formatted_content)
        italic_close = re.compile(r'\[\/i:([a-zA-Z0-9]+)\]', re.IGNORECASE)
        formatted_content = italic_close.sub(r'</i>', formatted_content)
        
        underline_open = re.compile(r'\[u:([a-zA-Z0-9]+)\]', re.IGNORECASE)
        formatted_content = underline_open.sub(r'<u>', formatted_content)
        underline_close = re.compile(r'\[\/u:([a-zA-Z0-9]+)\]', re.IGNORECASE)
        formatted_content = underline_close.sub(r'</u>', formatted_content)
        
        size_open = re.compile(r'\[size=([0-9]+):([a-zA-Z0-9]+)\]', re.IGNORECASE)
        formatted_content = size_open.sub(r'<span style="font-size:\1px;">', formatted_content)
        size_close = re.compile(r'\[\/size:([a-zA-Z0-9]+)\]', re.IGNORECASE)
        formatted_content = size_close.sub(r'</span>', formatted_content)
        
        quote_open = re.compile(r'\[quote:([a-zA-Z0-9]+)=\"([a-zA-Z0-9-._]+)\"\]', re.IGNORECASE)
        formatted_content = quote_open.sub(r'<blockquote>\2:<br/>', formatted_content)
        quote_close = re.compile(r'\[\/quote:([a-zA-Z0-9]+)\]', re.IGNORECASE)
        formatted_content = quote_close.sub(r'</blockquote>', formatted_content)
        
        youtube = re.compile(r'\[youtube\]http://(.+).youtube.com/watch\?v=([0-9A-Za-z-_]{11})(.*)\[/youtube\]', re.IGNORECASE)
        formatted_content = youtube.sub(r'<iframe width="560" height="315" src="https://www.youtube.com/embed/\2" frameborder="0" allowfullscreen></iframe>', formatted_content)
        
        img = re.compile(r'\[img:([a-zA-Z0-9]+)\](.+)\[\/img:([a-zA-Z0-9]+)\]', re.IGNORECASE)
        formatted_content = img.sub(r'<img src="\2" class="img-responsive">', formatted_content)
        
        smilies = [[1,":D","icon_biggrin.gif","Very Happy"],
        [2,":-D","icon_biggrin.gif","Very Happy"],
        [3,":grin:","icon_biggrin.gif","Very Happy"],
        [4,":)","icon_smile.gif","Smile"],
        [5,":-)","icon_smile.gif","Smile"],
        [6,":smile:","icon_smile.gif","Smile"],
        [7,":(","icon_sad.gif","Sad"],
        [8,":-(","icon_sad.gif","Sad"],
        [9,":sad:","icon_sad.gif","Sad"],
        [10,":o","icon_surprised.gif","Surprised"],
        [11,":-o","icon_surprised.gif","Surprised"],
        [12,":eek:","icon_surprised.gif","Surprised"],
        [13,":shock:","icon_eek.gif","Shocked"],
        [14,":?","icon_confused.gif","Confused"],
        [15,":-?","icon_confused.gif","Confused"],
        [16,":???:","icon_confused.gif","Confused"],
        [17,"8)","icon_cool.gif","Cool"],
        [18,"8-)","icon_cool.gif","Cool"],
        [19,":cool:","icon_cool.gif","Cool"],
        [20,":lol:","icon_lol.gif","Laughing"],
        [21,":x","icon_mad.gif","Mad"],
        [22,":-x","icon_mad.gif","Mad"],
        [23,":mad:","icon_mad.gif","Mad"],
        [24,":P","icon_razz.gif","Razz"],
        [25,":-P","icon_razz.gif","Razz"],
        [26,":razz:","icon_razz.gif","Razz"],
        [27,":oops:","icon_redface.gif","Embarassed"],
        [28,":cry:","icon_cry.gif","Crying or Very sad"],
        [29,":evil:","icon_evil.gif","Evil or Very Mad"],
        [30,":twisted:","icon_twisted.gif","Twisted Evil"],
        [31,":roll:","icon_rolleyes.gif","Rolling Eyes"],
        [32,":wink:","icon_wink.gif","Wink"],
        [33,";)","icon_wink.gif","Wink"],
        [34,";-)","icon_wink.gif","Wink"],
        [35,":!:","icon_exclaim.gif","Exclamation"],
        [36,":?:","icon_question.gif","Question"],
        [37,":idea:","icon_idea.gif","Idea"],
        [38,":arrow:","icon_arrow.gif","Arrow"],
        [39,":|","icon_neutral.gif","Neutral"],
        [40,":-|","icon_neutral.gif","Neutral"],
        [41,":neutral:","icon_neutral.gif","Neutral"],
        [42,":mrgreen:","icon_mrgreen.gif","Mr. Green"],
        [43,":-#","eusa_silenced.gif","Silenced"],
        [44,":-s","eusa_eh.gif","Eh?"],
        [45,":aiwebs_001:","aiwebs_001.gif","aiwebs_001"],
        [46,":aiwebs_002:","aiwebs_002.gif","aiwebs_002"],
        [47,":aiwebs_003:","aiwebs_003.gif","aiwebs_003"],
        [48,":aiwebs_004:","aiwebs_004.gif","aiwebs_004"],
        [49,":aiwebs_005:","aiwebs_005.gif","aiwebs_005"],
        [50,":aiwebs_006:","aiwebs_006.gif","aiwebs_006"],
        [51,":aiwebs_007:","aiwebs_007.gif","aiwebs_007"],
        [52,":aiwebs_008:","aiwebs_008.gif","aiwebs_008"],
        [53,":aiwebs_009:","aiwebs_009.gif","aiwebs_009"],
        [54,":aiwebs_010:","aiwebs_010.gif","aiwebs_010"],
        [55,":aiwebs_011:","aiwebs_011.gif","aiwebs_011"],
        [56,":aiwebs_012:","aiwebs_012.gif","aiwebs_012"],
        [57,":aiwebs_014:","aiwebs_014.gif","aiwebs_014"],
        [58,":aiwebs_015:","aiwebs_015.gif","aiwebs_015"],
        [59,":aiwebs_016:","aiwebs_016.gif","aiwebs_016"],
        [60,":aiwebs_017:","aiwebs_017.gif","aiwebs_017"],
        [61,":aiwebs_018:","aiwebs_018.gif","aiwebs_018"],
        [62,":aiwebs_019:","aiwebs_019.gif","aiwebs_019"],
        [63,":aiwebs_020:","aiwebs_020.gif","aiwebs_020"],
        [64,":aiwebs_021:","aiwebs_021.gif","aiwebs_021"],
        [65,":aiwebs_022:","aiwebs_022.gif","aiwebs_022"],
        [66,":aiwebs_023:","aiwebs_023.gif","aiwebs_023"],
        [67,":aiwebs_024:","aiwebs_024.gif","aiwebs_024"],
        [68,":aiwebs_025:","aiwebs_025.gif","aiwebs_025"],
        [69,":aiwebs_026:","aiwebs_026.gif","aiwebs_026"],
        [70,":aiwebs_027:","aiwebs_027.gif","aiwebs_027"],
        [71,":aiwebs_028:","aiwebs_028.gif","aiwebs_028"],
        [72,":aiwebs_029:","aiwebs_029.gif","aiwebs_029"],
        [73,":aiwebs_030:","aiwebs_030.gif","aiwebs_030"],
        [74,":aiwebs_033:","aiwebs_033.gif","aiwebs_033"]]
        
        for pack in smilies:
            img_url = '<img src="/static/img/smiles/%s" alt="%s">' % (pack[2], pack[3])
            formatted_content = formatted_content.replace(pack[1], img_url)
        
        #link = re.compile(r"(http://[^ ]+)")
        #formatted_content = link.sub(r'<a href="\1" rel="nofollow" target="_blank">\1</a>', formatted_content)
        
        url_open = re.compile(r'\[url=(.*?)\](.*?)\[\/url\]', re.IGNORECASE)
        formatted_content = url_open.sub(r'<a href="\1" rel="nofollow" target="_blank">\2</a>', formatted_content)
        
        #formatted_content = formatted_content.replace('\n', '<br />')
        return formatted_content


class Profile(models.Model):
    user = models.OneToOneField(User)
    posts = models.PositiveIntegerField(default=0)
    timezone = models.FloatField(default=0)
    avatar = models.CharField(max_length=100)
    birthday = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10)
    website = models.URLField(max_length=200)
    location = models.CharField(max_length=200)
    
    def __unicode__(self):
        return self.user.username
    
    def url(self):
        return "/user/%s" % self.id
    
    def avatar_url(self):
        if self.avatar:
            return "/static/img/avatars/%s" % self.avatar
        return "/static/img/avatar.gif"

User.profile = property(lambda u: Profile.objects.get_or_create(user=u)[0])
