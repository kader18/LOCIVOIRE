/**
 * Locivoire — Visite immersive (ambiance visite réelle)
 */
(function () {
    'use strict';

    var scenes = [];
    var currentSceneIndex = 0;
    var currentMode = 'look';
    var photoIndex = 0;
    var dragState = { active: false, startX: 0 };
    var curtainTimer = null;
    var splatViewer = null;
    var splatModulePromise = null;

    function $(id) {
        return document.getElementById(id);
    }

    function getCurrentScene() {
        return scenes[currentSceneIndex] || null;
    }

    function setHint(text) {
        var el = $('tour-hint');
        if (el) el.textContent = text;
    }

    function destroyAframe() {
        var container = $('aframe-viewer');
        if (!container) return;
        var scene = container.querySelector('a-scene');
        if (scene && scene.parentNode) {
            try { scene.parentNode.removeChild(scene); } catch (e) { /* ignore */ }
        }
        container.innerHTML = '';
        container.style.display = 'none';
    }

    function destroySplat() {
        var container = $('splat-viewer');
        if (splatViewer) {
            try {
                if (typeof splatViewer.dispose === 'function') splatViewer.dispose();
                else if (typeof splatViewer.destroy === 'function') splatViewer.destroy();
            } catch (e) { /* ignore */ }
            splatViewer = null;
        }
        if (container) {
            container.innerHTML = '';
            container.style.display = 'none';
        }
    }

    function showViewer(mode) {
        currentMode = mode;
        var a3d = $('aframe-viewer');
        var splat = $('splat-viewer');
        var photo = $('photo-viewer');
        var video = $('video-viewer');
        var pan = $('pannellum-viewer');
        if (pan) pan.style.display = 'none';
        if (a3d) a3d.style.display = mode === '3d' ? 'block' : 'none';
        if (splat) splat.style.display = mode === 'splat' ? 'block' : 'none';
        if (photo) photo.style.display = (mode === 'photos' || mode === 'look') ? 'flex' : 'none';
        if (video) video.style.display = mode === 'video' ? 'block' : 'none';

        var showPhotoUi = mode === 'photos' || mode === 'look' || mode === '3d';
        document.querySelectorAll('.iv-nav-fab').forEach(function (el) {
            el.style.display = showPhotoUi ? '' : 'none';
        });
        var thumbs = $('photo-thumbs');
        if (thumbs) thumbs.style.display = (mode === 'photos' || mode === 'look') ? '' : 'none';
        var spots = $('room-hotspots');
        if (spots) spots.style.display = (showPhotoUi || mode === 'splat') ? '' : 'none';
        var indicator = $('angle-indicator');
        if (indicator) indicator.style.display = showPhotoUi ? '' : 'none';

        document.querySelectorAll('[data-mode-btn]').forEach(function (btn) {
            var key = btn.getAttribute('data-mode-btn');
            var active = key === mode || (mode === 'look' && key === 'panorama');
            btn.classList.toggle('active', active);
        });
    }

    function showCurtain(title, subtitle) {
        var curtain = $('tour-curtain');
        var t = $('curtain-title');
        var s = $('curtain-sub');
        if (!curtain) return;
        if (t) t.textContent = title || '';
        if (s) s.textContent = subtitle || 'Vous entrez dans la pièce';
        curtain.classList.add('is-on');
        if (curtainTimer) clearTimeout(curtainTimer);
        curtainTimer = setTimeout(function () {
            curtain.classList.remove('is-on');
        }, 1100);
    }

    function updateProgress() {
        var el = $('tour-progress');
        if (el) el.textContent = (currentSceneIndex + 1) + ' / ' + scenes.length;
    }

    function updateRoomButtons() {
        document.querySelectorAll('.iv-room-btn').forEach(function (btn, i) {
            btn.classList.toggle('active', i === currentSceneIndex);
        });
        document.querySelectorAll('.immersive-tour__room-btn').forEach(function (btn, i) {
            btn.classList.toggle('active', i === currentSceneIndex);
        });
    }

    function renderHotspots() {
        var wrap = $('room-hotspots');
        if (!wrap) return;
        wrap.innerHTML = '';
        if (scenes.length < 2) return;

        var prev = (currentSceneIndex - 1 + scenes.length) % scenes.length;
        var next = (currentSceneIndex + 1) % scenes.length;

        function makeSpot(cls, label, index) {
            var b = document.createElement('button');
            b.type = 'button';
            b.className = 'iv-hotspot ' + cls;
            b.innerHTML = '<span class="iv-hotspot__dot"></span><span>Aller · ' + label + '</span>';
            b.addEventListener('click', function (e) {
                e.stopPropagation();
                loadScene(index, true);
            });
            wrap.appendChild(b);
        }

        makeSpot('iv-hotspot--left', scenes[prev].name, prev);
        makeSpot('iv-hotspot--right', scenes[next].name, next);

        if (scenes.length === 3) {
            var third = (currentSceneIndex + 2) % scenes.length;
            makeSpot('iv-hotspot--bottom', scenes[third].name, third);
        } else if (scenes.length > 3) {
            var topIdx = (currentSceneIndex + 2) % scenes.length;
            var bottomIdx = (currentSceneIndex + 3) % scenes.length;
            makeSpot('iv-hotspot--top', scenes[topIdx].name, topIdx);
            makeSpot('iv-hotspot--bottom', scenes[bottomIdx].name, bottomIdx);
        }
    }

    function renderPhotoView(withFade) {
        var scene = getCurrentScene();
        if (!scene || !scene.photos || !scene.photos.length) return;

        destroySplat();
        destroyAframe();
        if (currentMode !== 'look') showViewer('photos');
        else showViewer('look');

        setHint('Glissez pour un autre angle · pastilles dorées pour changer de pièce');

        var img = $('tour-main-img') || document.querySelector('#photo-viewer img.tour-main-photo');
        var indicator = $('angle-indicator');
        if (!img) return;

        var url = scene.photos[photoIndex];
        if (withFade) {
            img.classList.add('is-switching');
            setTimeout(function () {
                img.src = url;
                img.alt = scene.name;
                img.classList.remove('is-switching');
            }, 180);
        } else {
            img.src = url;
            img.alt = scene.name;
        }

        if (indicator) {
            indicator.textContent = scene.name + ' · vue ' + (photoIndex + 1) + ' / ' + scene.photos.length;
        }

        var thumbs = $('photo-thumbs');
        if (thumbs) {
            thumbs.innerHTML = '';
            scene.photos.forEach(function (src, i) {
                var b = document.createElement('button');
                b.type = 'button';
                b.className = 'iv-thumb immersive-tour__thumb' + (i === photoIndex ? ' active' : '');
                b.innerHTML = '<img src="' + src + '" alt="Vue ' + (i + 1) + '">';
                b.addEventListener('click', function (e) {
                    e.stopPropagation();
                    photoIndex = i;
                    renderPhotoView(true);
                });
                thumbs.appendChild(b);
            });
        }

        renderHotspots();
        updateProgress();
    }

    function loadLookAround(showIntro) {
        var scene = getCurrentScene();
        if (!scene || !scene.photos || !scene.photos.length) return;
        currentMode = 'look';
        if (showIntro) showCurtain(scene.name, 'Explorez la pièce à votre rythme');
        if (photoIndex >= scene.photos.length) photoIndex = 0;
        renderPhotoView(!!showIntro);
        bindPhotoDrag();
    }

    function loadPhotos() {
        currentMode = 'photos';
        photoIndex = 0;
        renderPhotoView(true);
        bindPhotoDrag();
    }

    function bindPhotoDrag() {
        var container = $('photo-viewer');
        if (!container || container.dataset.bound === '1') return;
        container.dataset.bound = '1';

        function onStart(x) {
            dragState.active = true;
            dragState.startX = x;
        }
        function onMove(x) {
            if (!dragState.active) return;
            var scene = getCurrentScene();
            if (!scene || !scene.photos || scene.photos.length < 2) return;
            var delta = x - dragState.startX;
            if (Math.abs(delta) > 85) {
                photoIndex = delta < 0
                    ? (photoIndex + 1) % scene.photos.length
                    : (photoIndex - 1 + scene.photos.length) % scene.photos.length;
                dragState.startX = x;
                renderPhotoView(true);
            }
        }
        function onEnd() { dragState.active = false; }

        container.addEventListener('mousedown', function (e) {
            if (e.target.closest('button')) return;
            onStart(e.clientX);
        });
        window.addEventListener('mousemove', function (e) { onMove(e.clientX); });
        window.addEventListener('mouseup', onEnd);
        container.addEventListener('touchstart', function (e) {
            if (e.touches[0]) onStart(e.touches[0].clientX);
        }, { passive: true });
        container.addEventListener('touchmove', function (e) {
            if (e.touches[0]) onMove(e.touches[0].clientX);
        }, { passive: true });
        container.addEventListener('touchend', onEnd);
    }

    function load3DScene() {
        var scene = getCurrentScene();
        if (!scene) return;
        destroySplat();
        destroyAframe();
        showViewer('3d');

        var container = $('aframe-viewer');
        if (!container) return;

        var photos = scene.photos || [];
        var pans = scene.panoramas || [];
        if (!photos.length && !pans.length) {
            container.innerHTML = '<div class="iv-empty"><p>Aucune photo pour cette pièce</p></div>';
            container.style.display = 'block';
            return;
        }

        if (typeof AFRAME === 'undefined') {
            container.innerHTML = '<div class="iv-empty"><p>Mode 3D indisponible</p></div>';
            container.style.display = 'block';
            return;
        }

        document.querySelectorAll('.iv-nav-fab').forEach(function (el) {
            el.style.display = photos.length > 1 ? '' : 'none';
        });
        var chip = $('angle-indicator');
        if (chip) {
            chip.style.display = '';
            chip.textContent = scene.name + (photos.length
                ? (' · angle ' + (photoIndex + 1) + ' / ' + photos.length)
                : ' · 360°');
        }

        // Panorama 360 réel
        if (pans.length && (!photos.length || scene.mode === 'panorama')) {
            if (photoIndex >= pans.length) photoIndex = 0;
            setHint('360° · ' + scene.name + ' — glissez pour regarder · molette pour zoomer · pastilles = changer de pièce');
            container.style.display = 'block';
            container.innerHTML = buildAframeRoomHtml({
                mainUrl: pans[photoIndex],
                isPano: true,
                roomName: scene.name
            });
            bindAframeRoom(container);
            return;
        }

        if (photoIndex >= photos.length) photoIndex = 0;
        setHint(
            '3D · ' + scene.name +
            ' — glissez pour regarder · molette pour zoomer · pastilles dorées = autre pièce · flèches = autre angle'
        );

        container.style.display = 'block';
        container.innerHTML = buildAframeRoomHtml({
            mainUrl: photos[photoIndex],
            isPano: false,
            roomName: scene.name
        });
        bindAframeRoom(container);
        updateProgress();
    }

    function buildAframeRoomHtml(opts) {
        // Une seule photo nette devant soi — plus de photos d'autres pièces en biais
        var mainVisual = opts.isPano
            ? '<a-sky src="#tex-main" rotation="0 -90 0"></a-sky>'
            : (
                '<a-plane src="#tex-main" width="14" height="8.4" position="0 1.65 -4.6" ' +
                'material="shader: flat; side: front; npot: true"></a-plane>'
            );

        return (
            '<a-scene embedded vr-mode-ui="enabled: false" loading-screen="enabled: false" ' +
            'renderer="antialias: true; colorManagement: true;" ' +
            'style="width:100%;height:100%;background:#070b14;">' +
            '<a-assets>' +
            '<img id="tex-main" src="' + opts.mainUrl + '" crossorigin="anonymous">' +
            '</a-assets>' +
            (opts.isPano ? '' : '<a-sky color="#0b1020"></a-sky>') +
            '<a-entity light="type: ambient; color: #ffffff; intensity: 1.15"></a-entity>' +
            '<a-plane rotation="-90 0 0" width="40" height="40" position="0 0 0" ' +
            'color="#0e1524" material="shader: flat"></a-plane>' +
            mainVisual +
            '<a-entity id="iv-cam-rig" position="0 1.6 0.4">' +
            '<a-camera id="iv-cam" look-controls="reverseMouseDrag: true; pointerLockEnabled: false" ' +
            'wasd-controls="enabled: false" fov="72" zoom="1"></a-camera>' +
            '</a-entity>' +
            '</a-scene>'
        );
    }

    var aframeWheelHandler = null;

    function bindAframeRoom(container) {
        if (aframeWheelHandler) {
            container.removeEventListener('wheel', aframeWheelHandler);
        }

        // Molette = zoom (FOV)
        aframeWheelHandler = function (e) {
            e.preventDefault();
            var cam = container.querySelector('#iv-cam');
            if (!cam) return;
            var fov = parseFloat(cam.getAttribute('fov')) || 72;
            fov += e.deltaY > 0 ? 4 : -4;
            fov = Math.max(48, Math.min(95, fov));
            cam.setAttribute('fov', fov);
        };
        container.addEventListener('wheel', aframeWheelHandler, { passive: false });

        // Pastilles HTML pour changer de pièce
        renderHotspots();
    }

    function loadVideo(url) {
        destroySplat();
        destroyAframe();
        showViewer('video');
        setHint('Vidéo filmée par le prestataire');
        var container = $('video-viewer');
        if (!container) return;
        container.innerHTML = '';
        var vid = document.createElement('video');
        vid.src = url;
        vid.controls = true;
        vid.playsInline = true;
        container.appendChild(vid);
    }

    function loadGaussianSplatModule() {
        if (!splatModulePromise) {
            splatModulePromise = import('https://esm.sh/@mkkellogg/gaussian-splats-3d@0.4.6')
                .catch(function () {
                    return import('https://cdn.jsdelivr.net/npm/@mkkellogg/gaussian-splats-3d@0.4.6/+esm');
                });
        }
        return splatModulePromise;
    }

    function loadSplatScene() {
        var scene = getCurrentScene();
        if (!scene || !scene.splats || !scene.splats.length) return;

        destroyAframe();
        destroySplat();
        showViewer('splat');
        setHint('Splat 3D · ' + scene.name + ' — glissez pour explorer la pièce reconstruite');

        var container = $('splat-viewer');
        if (!container) return;
        container.style.display = 'block';
        container.innerHTML = '<div class="iv-empty"><p>Chargement de la scène 3D…</p></div>';

        var url = scene.splats[0].url;
        loadGaussianSplatModule().then(function (mod) {
            var GaussianSplats3D = mod.default || mod;
            container.innerHTML = '';
            var viewer = new GaussianSplats3D.Viewer({
                rootElement: container,
                cameraUp: [0, -1, -0.6],
                initialCameraPosition: [-2.5, -1.5, 3.2],
                initialCameraLookAt: [0, 0, 0],
                sharedMemoryForWorkers: false,
                gpuAcceleratedSort: false
            });
            splatViewer = viewer;
            return viewer.addSplatScene(url, {
                showLoadingUI: true,
                progressiveLoad: true
            }).then(function () {
                renderHotspots();
                updateProgress();
            });
        }).catch(function (err) {
            console.error(err);
            container.innerHTML = '<div class="iv-empty"><p>Impossible de charger la scène splat.</p></div>';
        });
    }

    function updateModeButtons(scene) {
        var panBtn = $('btn-mode-panorama');
        var btn3d = $('btn-mode-3d');
        var photoBtn = $('btn-mode-photos');
        var videoBtn = $('btn-mode-video');
        var splatBtn = $('btn-mode-splat');
        var hasPhotos = scene.photos && scene.photos.length;
        var hasSplats = scene.splats && scene.splats.length;
        if (panBtn) panBtn.style.display = hasPhotos ? '' : 'none';
        if (btn3d) btn3d.style.display = hasPhotos ? '' : 'none';
        if (photoBtn) photoBtn.style.display = hasPhotos ? '' : 'none';
        if (videoBtn) videoBtn.style.display = scene.videos && scene.videos.length ? '' : 'none';
        if (splatBtn) splatBtn.style.display = hasSplats ? '' : 'none';
    }

    function loadScene(index, withCurtain) {
        if (index < 0 || index >= scenes.length) return;
        currentSceneIndex = index;
        photoIndex = 0;
        updateRoomButtons();
        updateProgress();

        var scene = getCurrentScene();
        if (!scene) return;
        updateModeButtons(scene);

        var stayInSplat = currentMode === 'splat' && scene.splats && scene.splats.length;
        var stayIn3d = currentMode === '3d';
        if (withCurtain) {
            showCurtain(
                scene.name,
                stayInSplat || stayIn3d ? 'Vous entrez dans un nouvel espace' : 'Vous entrez dans la pièce'
            );
        }

        if (stayInSplat || (scene.mode === 'splat' && scene.splats && scene.splats.length && currentMode !== '3d' && currentMode !== 'photos' && currentMode !== 'look' && currentMode !== 'video')) {
            loadSplatScene();
        } else if (stayIn3d && ((scene.photos && scene.photos.length) || (scene.panoramas && scene.panoramas.length))) {
            load3DScene();
        } else if (scene.splats && scene.splats.length && (!scene.photos || !scene.photos.length)) {
            loadSplatScene();
        } else if (scene.photos && scene.photos.length) {
            loadLookAround(false);
        } else if (scene.videos && scene.videos.length) {
            loadVideo(scene.videos[0].url);
        }
    }

    window.ImmersiveTour = {
        init: function (scenesData, startRoomId) {
            scenes = scenesData || [];
            if (!scenes.length) return;

            var startIndex = 0;
            if (startRoomId != null) {
                var found = scenes.findIndex(function (s) {
                    return String(s.room_id) === String(startRoomId);
                });
                if (found >= 0) startIndex = found;
            }

            document.querySelectorAll('.iv-room-btn').forEach(function (btn) {
                btn.addEventListener('click', function () {
                    var i = parseInt(btn.getAttribute('data-scene-index'), 10);
                    loadScene(i, true);
                });
            });

            // Compat anciennes classes
            document.querySelectorAll('.immersive-tour__room-btn').forEach(function (btn, i) {
                btn.addEventListener('click', function () { loadScene(i, true); });
            });

            if ($('btn-mode-panorama')) $('btn-mode-panorama').addEventListener('click', function () {
                destroySplat();
                loadLookAround(false);
            });
            if ($('btn-mode-3d')) $('btn-mode-3d').addEventListener('click', load3DScene);
            if ($('btn-mode-splat')) $('btn-mode-splat').addEventListener('click', loadSplatScene);
            if ($('btn-mode-photos')) $('btn-mode-photos').addEventListener('click', function () {
                destroySplat();
                loadPhotos();
            });
            if ($('btn-mode-video')) $('btn-mode-video').addEventListener('click', function () {
                var s = getCurrentScene();
                if (s && s.videos && s.videos.length) loadVideo(s.videos[0].url);
            });

            if ($('btn-prev-room')) $('btn-prev-room').addEventListener('click', function () {
                loadScene((currentSceneIndex - 1 + scenes.length) % scenes.length, true);
            });
            if ($('btn-next-room')) $('btn-next-room').addEventListener('click', function () {
                loadScene((currentSceneIndex + 1) % scenes.length, true);
            });
            if ($('btn-prev-photo')) $('btn-prev-photo').addEventListener('click', function () {
                var s = getCurrentScene();
                if (!s || !s.photos) return;
                photoIndex = (photoIndex - 1 + s.photos.length) % s.photos.length;
                if (currentMode === '3d') load3DScene();
                else renderPhotoView(true);
            });
            if ($('btn-next-photo')) $('btn-next-photo').addEventListener('click', function () {
                var s = getCurrentScene();
                if (!s || !s.photos) return;
                photoIndex = (photoIndex + 1) % s.photos.length;
                if (currentMode === '3d') load3DScene();
                else renderPhotoView(true);
            });

            showCurtain(scenes[startIndex].name, 'Bienvenue — commencez la visite');
            loadScene(startIndex, false);
            setTimeout(function () {
                var c = $('tour-curtain');
                if (c) c.classList.remove('is-on');
            }, 1400);
        }
    };
})();
