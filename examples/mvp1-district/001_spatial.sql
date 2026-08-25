BEGIN;

CREATE EXTENSION IF NOT EXISTS postgis;

CREATE TABLE IF NOT EXISTS awg_spatial_source (
    source_id text PRIMARY KEY,
    source_type text NOT NULL CHECK (source_type IN ('generated', 'imported', 'derived')),
    source_version text NOT NULL,
    checksum_sha256 char(64) NOT NULL,
    recorded_at timestamptz NOT NULL
);

CREATE TABLE IF NOT EXISTS awg_place (
    place_id text PRIMARY KEY,
    name text NOT NULL,
    geometry geometry(Point, 4326) NOT NULL,
    route_node_id text NOT NULL,
    source_id text NOT NULL REFERENCES awg_spatial_source(source_id)
);

CREATE TABLE IF NOT EXISTS awg_building (
    building_id text PRIMARY KEY,
    place_id text NOT NULL REFERENCES awg_place(place_id),
    footprint geometry(Polygon, 4326) NOT NULL,
    capacity integer NOT NULL CHECK (capacity >= 0),
    source_id text NOT NULL REFERENCES awg_spatial_source(source_id)
);

CREATE TABLE IF NOT EXISTS awg_building_entrance (
    entrance_id text PRIMARY KEY,
    building_id text NOT NULL REFERENCES awg_building(building_id),
    route_node_id text NOT NULL,
    geometry geometry(Point, 4326) NOT NULL,
    access_modes text[] NOT NULL
);

CREATE TABLE IF NOT EXISTS awg_route_node (
    route_node_id text PRIMARY KEY,
    geometry geometry(Point, 4326) NOT NULL,
    place_id text REFERENCES awg_place(place_id),
    entrance_id text REFERENCES awg_building_entrance(entrance_id)
);

CREATE TABLE IF NOT EXISTS awg_route_edge (
    route_edge_id text PRIMARY KEY,
    source_node_id text NOT NULL REFERENCES awg_route_node(route_node_id),
    target_node_id text NOT NULL REFERENCES awg_route_node(route_node_id),
    geometry geometry(LineString, 4326) NOT NULL,
    distance_m double precision NOT NULL CHECK (distance_m > 0),
    access_modes text[] NOT NULL,
    accessible boolean NOT NULL,
    source_id text NOT NULL REFERENCES awg_spatial_source(source_id)
);

CREATE INDEX IF NOT EXISTS awg_place_geometry_gix ON awg_place USING gist (geometry);
CREATE INDEX IF NOT EXISTS awg_building_footprint_gix ON awg_building USING gist (footprint);
CREATE INDEX IF NOT EXISTS awg_route_node_geometry_gix ON awg_route_node USING gist (geometry);
CREATE INDEX IF NOT EXISTS awg_route_edge_geometry_gix ON awg_route_edge USING gist (geometry);

COMMIT;
