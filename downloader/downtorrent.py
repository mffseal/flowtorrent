import os.path
import uuid

import libtorrent as lt
import time
import sys
import pathlib

import requests

download_dir = '/data'
filename = uuid.uuid4().hex

def test_torrent(link):
    ses = lt.session({'listen_interfaces': '0.0.0.0:6881'})
    atp = lt.add_torrent_params()

    # 如果是磁链
    if link.startswith('magnet:?'):
        atp = lt.parse_magnet_uri(link)
    # 如果是种子文件
    else:
        ti = lt.torrent_info(link)
        atp.ti = ti
    atp.save_path = '/Downloads'
    h = ses.add_torrent(atp)
    trackers = []

    # 更新DHT tracker服务器地址
    with open('trackers.list', 'r') as f:
        line = f.readline()
        idx = 1
        for idx in range(0,200):
            tracker = lt.announce_entry(line)
            tracker.tier = idx
            tracker.fail_limit = 2
            trackers.append(tracker)
    # 替换tracker服务器列表
    h.replace_trackers(trackers)
    s = h.status()
    print('starting', s.name)

    # 循环输出下载状态
    while not s.is_seeding:
        s = h.status()

        print('\r%.2f%% 已下载 (下载: %.1f kB/s 上传: %.1f kB/s peers: %d) %s' % (
            s.progress * 100, s.download_rate / 1000, s.upload_rate / 1000,
            s.num_peers, s.state), end=' ')

        alerts = ses.pop_alerts()
        for a in alerts:
            if a.category() & lt.alert.category_t.error_notification:
                print(a)
        sys.stdout.flush()
        time.sleep(2)
    print(h.status().name, 'complete')


if __name__ == '__main__':
    # test_torrent('./test.mkv.torrent')
    test_torrent('magnet:?xt=urn:btih:24d762e8cc9beb886f7ac09f89dfe49dcab78e03&dn=%e9%98%b3%e5%85%89%e7%94%b5%e5%bd%b1www.ygdy8.com.%e9%87%8e%e8%9b%ae%e4%ba%a4%e6%98%93.2021.BD.1080P.%e4%b8%ad%e5%ad%97.mkv&tr=udp%3a%2f%2ftracker.opentrackr.org%3a1337%2fannounce&tr=udp%3a%2f%2fexodus.desync.com%3a6969%2fannounce')
