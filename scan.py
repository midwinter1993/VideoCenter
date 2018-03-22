#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import yaml
import os
import re
import sys
import subprocess
import pprint
import codecs


def basename(filepath):
    return os.path.splitext(os.path.basename(filepath))[0]


def collect_videos(video_dir):
    videos = {}
    print 'Video PATH:', video_dir
    for root, dirs, files in os.walk(unicode(video_dir, 'utf-8')):
        for f in files:
            if f.endswith('.mp4') or f.endswith('.avi'):
                video_path = os.path.join(root, f)
                video_codec = get_video_codes(video_path)

                if 'h264' not in video_codec:
                    print '%s ==> %s' % (video_path, str(video_codec))
                else:
                    videos[basename(f)] = video_path
    return videos


def get_video_codes(video_path):
    p = subprocess.Popen(['avprobe', '-show_streams', '-i', video_path],
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
    stdout, stderr = p.communicate()

    codec_names = re.findall(r'codec_name=(.*)', stdout)

    #  video_codec = codec_names[0]

    return codec_names


def save_json(data, filepath):
    with codecs.open(filepath, 'w', 'utf-8') as fd:
        fd.write(json.dumps(data,
                            ensure_ascii=False,
                            indent=4,
                            sort_keys=True))


def save_yaml(data, filepath):
    with codecs.open(filepath, 'w', 'utf-8') as fd:
        fd.write(yaml.dump(data))


def append_save_json(data, filepath):
    old_data = json.load(open(filepath))
    old_data.update(data)
    save_json(old_data, filepath)


if __name__ == "__main__":
    args = sys.argv[:]

    if len(args) != 3:
        print 'Usage scan [-a|-s] <video-dir>'
        sys.exit(0)
    opt = args[1]
    video_dir = args[2]

    if opt == '-s':
        videos = collect_videos(video_dir)
        print 'Scan: #', len(videos)
        save_json(videos, u'./videos/data.json')
    elif opt == '-a':
        videos = collect_videos(video_dir)
        print 'Scan: #', len(videos)
        append_save_json(videos, u'./videos/data.json')
