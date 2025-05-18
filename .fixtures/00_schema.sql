--
-- PostgreSQL database dump
--

-- Dumped from database version 17.5 (Debian 17.5-1.pgdg120+1)
-- Dumped by pg_dump version 17.5 (Debian 17.5-1.pgdg120+1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: postgis; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS postgis WITH SCHEMA public;


--
-- Name: EXTENSION postgis; Type: COMMENT; Schema: -; Owner:
--

COMMENT ON EXTENSION postgis IS 'PostGIS geometry and geography spatial types and functions';


--
-- Name: check_activity_nested_level(); Type: FUNCTION; Schema: public; Owner: debug
--

CREATE FUNCTION public.check_activity_nested_level() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
    IF EXISTS(
            select a3.* from public.activity a1
            join public.activity a2 on a1.activity_id = a2.id
            join public.activity a3 on a2.activity_id = a3.id
            where a1.id = NEW.activity_id
        )
        then RAISE EXCEPTION 'Maximum nesting level exceeded';
    END IF;

    RETURN NEW;

END;
$$;


ALTER FUNCTION public.check_activity_nested_level() OWNER TO debug;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: activity; Type: TABLE; Schema: public; Owner: debug
--

CREATE TABLE public.activity (
    id integer NOT NULL,
    title character varying NOT NULL,
    activity_id integer
);


ALTER TABLE public.activity OWNER TO debug;

--
-- Name: activity_id_seq; Type: SEQUENCE; Schema: public; Owner: debug
--

CREATE SEQUENCE public.activity_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.activity_id_seq OWNER TO debug;

--
-- Name: activity_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: debug
--

ALTER SEQUENCE public.activity_id_seq OWNED BY public.activity.id;


--
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: debug
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE public.alembic_version OWNER TO debug;

--
-- Name: building; Type: TABLE; Schema: public; Owner: debug
--

CREATE TABLE public.building (
    id uuid NOT NULL,
    address character varying NOT NULL,
    coordinates public.geography(Point,4326) NOT NULL
);


ALTER TABLE public.building OWNER TO debug;

--
-- Name: org_activity; Type: TABLE; Schema: public; Owner: debug
--

CREATE TABLE public.org_activity (
    activity_id integer,
    organization_id uuid
);


ALTER TABLE public.org_activity OWNER TO debug;

--
-- Name: organization; Type: TABLE; Schema: public; Owner: debug
--

CREATE TABLE public.organization (
    id uuid NOT NULL,
    name character varying NOT NULL,
    phone_numbers character varying[] NOT NULL,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL,
    building_id uuid NOT NULL
);


ALTER TABLE public.organization OWNER TO debug;

--
-- Name: activity id; Type: DEFAULT; Schema: public; Owner: debug
--

ALTER TABLE ONLY public.activity ALTER COLUMN id SET DEFAULT nextval('public.activity_id_seq'::regclass);


--
-- Name: activity activity_child_title_un; Type: CONSTRAINT; Schema: public; Owner: debug
--

ALTER TABLE ONLY public.activity
    ADD CONSTRAINT activity_child_title_un UNIQUE (title, activity_id);


--
-- Name: activity activity_pkey; Type: CONSTRAINT; Schema: public; Owner: debug
--

ALTER TABLE ONLY public.activity
    ADD CONSTRAINT activity_pkey PRIMARY KEY (id);


--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: debug
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- Name: building building_coordinates_key; Type: CONSTRAINT; Schema: public; Owner: debug
--

ALTER TABLE ONLY public.building
    ADD CONSTRAINT building_coordinates_key UNIQUE (coordinates);


--
-- Name: building building_pkey; Type: CONSTRAINT; Schema: public; Owner: debug
--

ALTER TABLE ONLY public.building
    ADD CONSTRAINT building_pkey PRIMARY KEY (id);


--
-- Name: org_activity org_activity_un; Type: CONSTRAINT; Schema: public; Owner: debug
--

ALTER TABLE ONLY public.org_activity
    ADD CONSTRAINT org_activity_un UNIQUE (activity_id, organization_id);


--
-- Name: organization organization_pkey; Type: CONSTRAINT; Schema: public; Owner: debug
--

ALTER TABLE ONLY public.organization
    ADD CONSTRAINT organization_pkey PRIMARY KEY (id);


--
-- Name: idx_building_coordinates; Type: INDEX; Schema: public; Owner: debug
--

CREATE INDEX idx_building_coordinates ON public.building USING gist (coordinates);


--
-- Name: ix_activity_id; Type: INDEX; Schema: public; Owner: debug
--

CREATE INDEX ix_activity_id ON public.activity USING btree (id);


--
-- Name: activity check_activity_insert_trigger; Type: TRIGGER; Schema: public; Owner: debug
--

CREATE TRIGGER check_activity_insert_trigger BEFORE INSERT ON public.activity FOR EACH ROW EXECUTE FUNCTION public.check_activity_nested_level();


--
-- Name: activity activity_activity_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: debug
--

ALTER TABLE ONLY public.activity
    ADD CONSTRAINT activity_activity_id_fkey FOREIGN KEY (activity_id) REFERENCES public.activity(id) ON DELETE SET NULL;


--
-- Name: org_activity org_activity_activity_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: debug
--

ALTER TABLE ONLY public.org_activity
    ADD CONSTRAINT org_activity_activity_id_fkey FOREIGN KEY (activity_id) REFERENCES public.activity(id) ON DELETE CASCADE;


--
-- Name: org_activity org_activity_organization_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: debug
--

ALTER TABLE ONLY public.org_activity
    ADD CONSTRAINT org_activity_organization_id_fkey FOREIGN KEY (organization_id) REFERENCES public.organization(id) ON DELETE CASCADE;


--
-- Name: organization organization_building_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: debug
--

ALTER TABLE ONLY public.organization
    ADD CONSTRAINT organization_building_id_fkey FOREIGN KEY (building_id) REFERENCES public.building(id) ON DELETE SET NULL;


--
-- PostgreSQL database dump complete
--

