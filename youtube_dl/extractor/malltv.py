# coding: utf-8
from __future__ import unicode_literals

from .common import InfoExtractor
from ..utils import parse_duration


class MallTVIE(InfoExtractor):
    _VALID_URL = r'https?://(?:www\.)?mall\.tv/(?:.+/)?(?P<id>.+)'
    _TESTS = [
        {
            'url': ('https://www.mall.tv/18-miliard-pro-neziskovky'
                    '-opravdu-jsou-sportovci-nebo-clovek-v-tisni-pijavice'),
            'md5': '5235290504d20a27a19dd3915b1167b4',
            'info_dict': {
                'id': ('18-miliard-pro-neziskovky-opravdu-jsou-sportovci-nebo-'
                       'clovek-v-tisni-pijavice'),
                'ext': 'mp4',
                'title': ('18 miliard pro neziskovky. Opravdu jsou sportovci '
                          'nebo Člověk v tísni pijavice?'),
                'description': ('Pokud někdo hospodaří s penězmi daňových '
                                'poplatníků, pak logicky chceme vědět, jak s '
                                'nimi nakládá. Objem dotací pro neziskovky '
                                'roste, ale opravdu jsou tyto organizace '
                                '„pijavice", jak o nich hovoří And')
                },
        },
        {
            'url': ('https://www.mall.tv/kdo-to-plati/18-miliard-pro-neziskovky'
                    '-opravdu-jsou-sportovci-nebo-clovek-v-tisni-pijavice'),
            'md5': '5235290504d20a27a19dd3915b1167b4',
            'info_dict': {
                'id': ('18-miliard-pro-neziskovky-opravdu-jsou-sportovci-nebo-'
                       'clovek-v-tisni-pijavice'),
                'ext': 'mp4',
                'title': ('18 miliard pro neziskovky. Opravdu jsou sportovci '
                          'nebo Člověk v tísni pijavice?'),
                'description': ('Pokud někdo hospodaří s penězmi daňových '
                                'poplatníků, pak logicky chceme vědět, jak s '
                                'nimi nakládá. Objem dotací pro neziskovky '
                                'roste, ale opravdu jsou tyto organizace '
                                '„pijavice", jak o nich hovoří And')
                }
        },
    ]

    def _real_extract(self, url):
        video_id = self._match_id(url)
        webpage = self._download_webpage(url, video_id)
        JSON_LD_RE = (r'(?is)<script[^>]+type=([\"\'])?application/ld\+json>.*'
                      '(?P<json_ld>{.+}).*</script>')
        json_ld = self._search_regex(JSON_LD_RE, webpage, 'JSON_LD',
                                     group='json_ld')
        if not json_ld:
            info = {}
        else:
            info = self._json_ld(json_ld, video_id)

        format_url = self._html_search_regex(
            r'<source src=([\"\'])?(.+index)\s',
            webpage,
            'm3u8 URL')
        formats = self._extract_m3u8_formats(format_url+'.m3u8',
                                             video_id, 'mp4')
        self._sort_formats(formats)
        title = info.get('title', self._og_search_title(webpage, fatal=False))
        thumbnail = info.get('thumbnailUrl', self._og_search_thumbnail(webpage))
        return {
            'id': video_id,
            'title': title,
            'thumbnail': thumbnail,
            'description': self._og_search_description(webpage),
            'duration': parse_duration(info.get('duration')),
            'formats': formats
        }
