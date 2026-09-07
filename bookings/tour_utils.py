"""Construction des données de visite immersive à partir des médias uploadés."""

import json


def _image_url(request, image_field):
    if not image_field:
        return None
    return request.build_absolute_uri(image_field.url)


def build_immersive_tour_data(request, property_obj):
    """
    Construit la structure de visite pièce par pièce à partir des photos/vidéos/splats.
    Priorité par pièce : splat prêt > panorama 360° > photos multiples > vidéo.
    """
    rooms = list(property_obj.rooms.all().order_by('order', 'floor_number', 'name'))
    images = list(property_obj.images.select_related('room').all())
    videos = list(property_obj.videos.select_related('room').all())
    splats = list(
        property_obj.splats.filter(status='ready')
        .exclude(splat_file='')
        .select_related('room')
    )

    images_by_room = {}
    panoramas_by_room = {}
    videos_by_room = {}
    splats_by_room = {}

    for img in images:
        key = img.room_id or 0
        if img.image_type == 'panorama_360':
            panoramas_by_room.setdefault(key, []).append(img)
        else:
            images_by_room.setdefault(key, []).append(img)

    for vid in videos:
        key = vid.room_id or 0
        videos_by_room.setdefault(key, []).append(vid)

    for sp in splats:
        if not sp.splat_file:
            continue
        key = sp.room_id or 0
        splats_by_room.setdefault(key, []).append(sp)

    scenes = []
    room_keys = set()
    room_keys.update(panoramas_by_room.keys())
    room_keys.update(images_by_room.keys())
    room_keys.update(videos_by_room.keys())
    room_keys.update(splats_by_room.keys())
    room_keys.update(r.pk for r in rooms)

    room_map = {r.pk: r for r in rooms}
    room_map[0] = None

    def room_label(room_id):
        if room_id == 0 or room_id not in room_map or room_map[room_id] is None:
            return 'Vue générale'
        return room_map[room_id].name

    def room_type(room_id):
        if room_id == 0 or room_id not in room_map or room_map[room_id] is None:
            return 'general'
        return room_map[room_id].room_type

    ordered_keys = []
    for room in rooms:
        if room.pk in room_keys:
            ordered_keys.append(room.pk)
    if not ordered_keys and 0 in room_keys:
        ordered_keys.append(0)
    for key in sorted(room_keys):
        if key not in ordered_keys and key != 0:
            ordered_keys.append(key)

    for room_id in ordered_keys:
        pans = panoramas_by_room.get(room_id, [])
        photos = images_by_room.get(room_id, [])
        vids = videos_by_room.get(room_id, [])
        room_splats = splats_by_room.get(room_id, [])

        if not pans and not photos and not vids and not room_splats:
            continue

        scene = {
            'id': f'room-{room_id}',
            'room_id': room_id,
            'name': room_label(room_id),
            'room_type': room_type(room_id),
            'panoramas': [_image_url(request, p.image) for p in pans],
            'photos': [_image_url(request, p.image) for p in photos],
            'videos': [
                {
                    'url': request.build_absolute_uri(v.video.url),
                    'title': v.title or 'Visite vidéo',
                    'type': v.video_type,
                }
                for v in vids
            ],
            'splats': [
                {
                    'url': request.build_absolute_uri(s.splat_file.url),
                    'title': s.title or room_label(room_id),
                    'id': s.pk,
                }
                for s in room_splats
            ],
        }

        if room_splats:
            scene['mode'] = 'splat'
            scene['primary'] = scene['splats'][0]['url']
        elif photos:
            scene['mode'] = 'photos'
            scene['primary'] = scene['photos'][0]
            scene['panoramas'] = []
        elif pans:
            scene['mode'] = 'panorama'
            scene['primary'] = scene['panoramas'][0]
        elif vids:
            scene['mode'] = 'video'
            scene['primary'] = scene['videos'][0]['url']
        else:
            continue

        scenes.append(scene)

    return {
        'scenes': scenes,
        'scenes_json': json.dumps(scenes),
        'has_panoramas': any(s.get('mode') == 'panorama' for s in scenes),
        'has_photos': any(s.get('photos') for s in scenes),
        'has_videos': any(s.get('videos') for s in scenes),
        'has_splats': any(s.get('splats') for s in scenes),
        'has_immersive_tour': len(scenes) > 0,
    }
