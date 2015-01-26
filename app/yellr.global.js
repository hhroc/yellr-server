// We are currently using mapbox to create our geofencing maps. Mapbox requires
// an account and API key. Please see https://www.mapbox.com for obtaining an
// API key (it's free).
window.MAPBOX_API_KEY = 'pk.eyJ1Ijoibm9sc2tpIiwiYSI6IlhTS3lpb1EifQ.jPZ2V9H2FOZX5rDi8sh1eg';
window.MAPBOX_MAP_ID = 'nolski.kp851mlm';

if(window.MAPBOX_API_KEY == '<your_api_key_here>') {
    console.error('WARNING: Mapbox API key is not set. See app/yellr.global.js' +
                'for more info.');
}

if(window.MAPBOX_MAP_ID == '<your_map_id_here>') {
    console.error('WARNING: Mapbox map id is not set. See app/yellr.global.js' +
                'for more info.');
}
