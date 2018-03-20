#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import yaml
import os
import re
import sys
import subprocess


def basename(filepath):
    return os.path.splitext(os.path.basename(filepath))[0]


def collect_videos(video_dir):
    videos = {}
    print 'Video PATH:', video_dir
    for root, dirs, files in os.walk(video_dir):
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
    with open(filepath, 'w') as fd:
        fd.write(json.dumps(data,
                            ensure_ascii=False,
                            indent=4,
                            sort_keys=True).encode('utf8'))


def save_yaml(data, filepath):
    with open(filepath, 'w') as fd:
        fd.write(yaml.dump(data))



VIDEO_DIR = u'/media/dongjie/0123-4567/vedio'

if __name__ == "__main__":
    videos = collect_videos(VIDEO_DIR)
    print 'Scan: #', len(videos)
    save_json(videos, './videos/data.json')
