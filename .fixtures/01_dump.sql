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
-- Data for Name: activity; Type: TABLE DATA; Schema: public; Owner: debug
--

COPY public.activity (id, title, activity_id) FROM stdin;
1	Еда	\N
2	Мясная продукция	1
3	Молочная продукция	1
4	Алкогольная продукция	1
11	Хлеб	5
12	Батон	5
13	Выпечка	5
5	Хлебо-булочная продукция	1
6	Пиво	4
7	Водка	4
10	Вино	4
14	Автомобили	\N
15	Грузовые	14
16	Легковые	14
17	Запчасти	15
18	Инструменты	15
19	Запчасти	16
20	Аксессуары	16
21	Одежда	\N
22	Мужская одежда	21
23	Женская одежда	21
24	Костюмы	22
25	Спецодежда мужская	22
26	Платья	23
27	Спецодежда женская	23
\.


--
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: debug
--

COPY public.alembic_version (version_num) FROM stdin;
a305d5896f20
\.


--
-- Data for Name: building; Type: TABLE DATA; Schema: public; Owner: debug
--

COPY public.building (id, address, coordinates) FROM stdin;
1444a266-ee1f-4820-af5e-024b2120679a	Минск, улица Свердлова, 11	0101000020E61000006107DFAB5AF24A40918B4D2B858E3B40
01c80415-d51b-4464-9d79-05f0d338703f	Минск, улица Кирова, 8/3-1	0101000020E6100000692F2F707DF24A403E1CEBE2368E3B40
699b2637-8e6e-40b2-a9a4-8579ceffcedb	Минск, улица Свердлова, 32	0101000020E610000015419A400FF24A406E279F1EDB8E3B40
616b42e0-95f1-4719-9915-e41cd54c122e	Минск, улица Свердлова, 23/4	0101000020E610000067E88FA7E9F14A4047637B2DE88F3B40
98858f2f-749b-4aa0-b6e6-111afd95e1bd	Минский район, Заславль, улица Путейко, 1	0101000020E61000003F00F75CAA004B40AE230ED940483B40
8f37c285-8bbc-4add-93ef-6ba76f553a12	Минский район, Новодворский сельсовет, деревня Королищевичи, Центральная улица, 86Б	0101000020E61000007BE951DB8AE64A407226FBE769B23B40
303b7bd5-a5c7-429a-a4f5-192bbbc61b91	Минская область, Жодино, улица 40 лет Октября, 4	0101000020E610000073C65E80810C4B40C24D7FF623513C40
\.


--
-- Data for Name: org_activity; Type: TABLE DATA; Schema: public; Owner: debug
--

COPY public.org_activity (activity_id, organization_id) FROM stdin;
15	d38caddb-6e36-4cac-afbd-aa2d74e8023a
17	d38caddb-6e36-4cac-afbd-aa2d74e8023a
18	d38caddb-6e36-4cac-afbd-aa2d74e8023a
11	c6e48a87-902a-4276-8b19-1a735a3be663
12	c6e48a87-902a-4276-8b19-1a735a3be663
13	c6e48a87-902a-4276-8b19-1a735a3be663
11	e3abce53-8691-4d2f-95a7-d06ffc4b711d
12	e3abce53-8691-4d2f-95a7-d06ffc4b711d
7	efb081c6-614c-472e-9c43-1d102d0f312d
10	efb081c6-614c-472e-9c43-1d102d0f312d
6	1946305b-2921-410d-91a9-804e03ef4cbb
16	ee3e39af-23cf-4e06-92fa-420f60370d60
19	ee3e39af-23cf-4e06-92fa-420f60370d60
20	ee3e39af-23cf-4e06-92fa-420f60370d60
23	a11bab4a-d836-4184-8e63-626b5dad5c6b
26	a11bab4a-d836-4184-8e63-626b5dad5c6b
27	a11bab4a-d836-4184-8e63-626b5dad5c6b
22	1f791040-9c2f-473a-9006-21db8c3f9aeb
24	1f791040-9c2f-473a-9006-21db8c3f9aeb
25	1f791040-9c2f-473a-9006-21db8c3f9aeb
22	a7ea40eb-08c0-4f08-8291-3f589913138d
23	a7ea40eb-08c0-4f08-8291-3f589913138d
2	5eb07f54-d2e4-4612-a8c5-3e729fac648a
3	5eb07f54-d2e4-4612-a8c5-3e729fac648a
\.


--
-- Data for Name: organization; Type: TABLE DATA; Schema: public; Owner: debug
--

COPY public.organization (id, name, phone_numbers, created_at, updated_at, building_id) FROM stdin;
d38caddb-6e36-4cac-afbd-aa2d74e8023a	Белорусский автомобильный завод	{"+375 (17) 278-88-25","+375 (17) 278-88-26","+375 (17) 278-88-27","+375 (17) 278-88-28"}	2025-05-18 07:58:57.263165	2025-05-18 07:58:57.263165	303b7bd5-a5c7-429a-a4f5-192bbbc61b91
c6e48a87-902a-4276-8b19-1a735a3be663	Тьерри пекарня	{"+375 (17) 278-88-24"}	2025-05-18 08:00:10.011175	2025-05-18 08:00:10.011175	616b42e0-95f1-4719-9915-e41cd54c122e
e3abce53-8691-4d2f-95a7-d06ffc4b711d	Минскхлебпром	{"+375 (17) 278-88-23"}	2025-05-18 08:00:38.201588	2025-05-18 08:00:38.201588	616b42e0-95f1-4719-9915-e41cd54c122e
efb081c6-614c-472e-9c43-1d102d0f312d	МИНСК КРИСТАЛЛ	{"+375 (17) 278-88-20","+375 (17) 278-88-21","+375 (17) 278-88-22"}	2025-05-18 08:01:33.267261	2025-05-18 08:01:33.267261	699b2637-8e6e-40b2-a9a4-8579ceffcedb
1946305b-2921-410d-91a9-804e03ef4cbb	Аливария	{"+375 (17) 278-88-17","+375 (17) 278-88-18","+375 (17) 278-88-19"}	2025-05-18 08:03:01.743855	2025-05-18 08:03:01.743855	699b2637-8e6e-40b2-a9a4-8579ceffcedb
ee3e39af-23cf-4e06-92fa-420f60370d60	МИНСКИЙ АВТОМОБИЛЬНЫЙ ЗАВОД	{"+375 (17) 278-88-15","+375 (17) 278-88-16"}	2025-05-18 08:04:24.710516	2025-05-18 08:04:24.710516	8f37c285-8bbc-4add-93ef-6ba76f553a12
a11bab4a-d836-4184-8e63-626b5dad5c6b	ТЭЛСТАЙЛ. Женская одежда	{"+375 (17) 278-88-13","+375 (17) 278-88-14"}	2025-05-18 08:05:26.612582	2025-05-18 08:05:26.612582	01c80415-d51b-4464-9d79-05f0d338703f
1f791040-9c2f-473a-9006-21db8c3f9aeb	ГОЛДСТАЙЛ. Мужская одежда	{"+375 (17) 278-88-11","+375 (17) 278-88-12"}	2025-05-18 08:06:04.550948	2025-05-18 08:06:04.550948	01c80415-d51b-4464-9d79-05f0d338703f
a7ea40eb-08c0-4f08-8291-3f589913138d	ЗОЛОТОЕ РУНО	{"+375 (17) 278-88-09","+375 (17) 278-88-10"}	2025-05-18 08:07:24.017445	2025-05-18 08:07:24.017445	1444a266-ee1f-4820-af5e-024b2120679a
5eb07f54-d2e4-4612-a8c5-3e729fac648a	Минский мясокомбинат	{"+375 (17) 278-88-07","+375 (17) 278-88-08"}	2025-05-18 08:08:21.606641	2025-05-18 08:08:21.606641	98858f2f-749b-4aa0-b6e6-111afd95e1bd
\.


--
-- Data for Name: spatial_ref_sys; Type: TABLE DATA; Schema: public; Owner: debug
--

COPY public.spatial_ref_sys (srid, auth_name, auth_srid, srtext, proj4text) FROM stdin;
\.


--
-- Name: activity_id_seq; Type: SEQUENCE SET; Schema: public; Owner: debug
--

SELECT pg_catalog.setval('public.activity_id_seq', 27, true);


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
