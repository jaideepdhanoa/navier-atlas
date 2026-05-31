// Offline MapLibre GL stub, served in place of the CDN bundle during tests.
// index.html is one large inline script; a throwing `new maplibregl.Map()` would
// halt it before the bottom-sheet code runs. This provides a forgiving, no-op
// `maplibregl` global so the page's synchronous setup completes. Map tiles/layers
// are NOT rendered — these tests cover the render-surface UI, not the map itself.
(function () {
  var noop = function () { return this; };
  function makeMap() {
    var handlers = {};
    var canvas = document.createElement('canvas');
    var base = {
      on: function (ev, a, b) { var cb = b || a; (handlers[ev] = handlers[ev] || []).push(cb); return this; },
      once: function (ev, a, b) { var cb = b || a; (handlers[ev] = handlers[ev] || []).push(cb); return this; },
      off: noop,
      // Deliberately never fired: the page's heavy layer-build runs inside 'load',
      // which we don't need and which would only add flakiness. Tests dismiss the
      // #loading overlay directly instead.
      fire: function (ev) { (handlers[ev] || []).forEach(function (cb) { try { cb({}); } catch (e) {} }); return this; },
      addControl: noop, removeControl: noop,
      addSource: noop, removeSource: noop, addLayer: noop, removeLayer: noop, moveLayer: noop,
      setPaintProperty: noop, setLayoutProperty: noop, setFilter: noop, setData: noop, setFeatureState: noop,
      getLayer: function () { return undefined; }, getSource: function () { return undefined; },
      getCanvas: function () { return canvas; }, getContainer: function () { return document.getElementById('map'); },
      getCenter: function () { return { lng: 0, lat: 0 }; }, getZoom: function () { return 2; },
      getBounds: function () { return { getNorthEast: function () { return { lng: 0, lat: 0 }; }, getSouthWest: function () { return { lng: 0, lat: 0 }; } }; },
      resize: noop, flyTo: noop, jumpTo: noop, easeTo: noop, fitBounds: noop, panTo: noop, zoomTo: noop,
      queryRenderedFeatures: function () { return []; },
      project: function () { return { x: 0, y: 0 }; }, unproject: function () { return { lng: 0, lat: 0 }; },
      remove: noop, loaded: function () { return true; }, isStyleLoaded: function () { return true; },
    };
    return new Proxy(base, { get: function (t, p) { return (p in t) ? t[p] : noop; } });
  }

  function Ctrl() {}
  Ctrl.prototype.onAdd = function () { return document.createElement('div'); };
  Ctrl.prototype.onRemove = noop;

  function Popup() {}
  ['setLngLat', 'setHTML', 'setDOMContent', 'addTo', 'remove', 'setOffset', 'on', 'setText'].forEach(function (m) {
    Popup.prototype[m] = noop;
  });

  function Bounds() {}
  Bounds.prototype.extend = function () { return this; };
  Bounds.prototype.getCenter = function () { return { lng: 0, lat: 0 }; };
  Bounds.prototype.isEmpty = function () { return false; };

  window.maplibregl = { Map: makeMap, NavigationControl: Ctrl, Popup: Popup, Marker: Ctrl, LngLatBounds: Bounds };
})();
