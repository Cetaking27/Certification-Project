--
-- PostgreSQL database dump
--

-- Dumped from database version 12.9 (Ubuntu 12.9-2.pgdg20.04+1)
-- Dumped by pg_dump version 12.9 (Ubuntu 12.9-2.pgdg20.04+1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

DROP DATABASE universe;
--
-- Name: universe; Type: DATABASE; Schema: -; Owner: freecodecamp
--

CREATE DATABASE universe WITH TEMPLATE = template0 ENCODING = 'UTF8' LC_COLLATE = 'C.UTF-8' LC_CTYPE = 'C.UTF-8';


ALTER DATABASE universe OWNER TO freecodecamp;

\connect universe

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: galaxy; Type: TABLE; Schema: public; Owner: freecodecamp
--

CREATE TABLE public.galaxy (
    galaxy_id integer NOT NULL,
    name character varying(30),
    galaxy_name text,
    galaxy_lighting boolean NOT NULL,
    galaxy_darken boolean NOT NULL,
    galaxy_numb numeric(3,2),
    galaxy_character integer,
    galaxy_show integer NOT NULL
);


ALTER TABLE public.galaxy OWNER TO freecodecamp;

--
-- Name: moon; Type: TABLE; Schema: public; Owner: freecodecamp
--

CREATE TABLE public.moon (
    moon_id integer NOT NULL,
    name character varying(20),
    moon_name text,
    moon_lighting boolean NOT NULL,
    moon_darken boolean NOT NULL,
    moon_numb numeric(5,2) NOT NULL,
    planet_id integer,
    moon_show integer NOT NULL
);


ALTER TABLE public.moon OWNER TO freecodecamp;

--
-- Name: planet; Type: TABLE; Schema: public; Owner: freecodecamp
--

CREATE TABLE public.planet (
    planet_id integer NOT NULL,
    name character varying(10),
    planet_name text,
    planet_lighting boolean NOT NULL,
    planet_darken boolean NOT NULL,
    planet_numb numeric NOT NULL,
    star_id integer,
    planet_show integer NOT NULL
);


ALTER TABLE public.planet OWNER TO freecodecamp;

--
-- Name: star; Type: TABLE; Schema: public; Owner: freecodecamp
--

CREATE TABLE public.star (
    star_id integer NOT NULL,
    name character varying(15),
    star_name text,
    star_lighting boolean NOT NULL,
    star_darken boolean NOT NULL,
    star_numb numeric(5,2) NOT NULL,
    galaxy_id integer NOT NULL,
    star_show integer NOT NULL
);


ALTER TABLE public.star OWNER TO freecodecamp;

--
-- Name: system; Type: TABLE; Schema: public; Owner: freecodecamp
--

CREATE TABLE public.system (
    system_id integer NOT NULL,
    name character varying(30),
    character_sys integer NOT NULL,
    sys_show integer,
    system_blut boolean,
    system_blink boolean
);


ALTER TABLE public.system OWNER TO freecodecamp;

--
-- Data for Name: galaxy; Type: TABLE DATA; Schema: public; Owner: freecodecamp
--

INSERT INTO public.galaxy VALUES (1, 'galaxy_A1', 'aarone', true, false, 9.00, 655, 265);
INSERT INTO public.galaxy VALUES (2, 'galaxy_A2', 'birone', false, false, 8.00, 55, 265);
INSERT INTO public.galaxy VALUES (3, 'galaxy_A3', 'cyclone', true, true, 7.00, 155, 266);
INSERT INTO public.galaxy VALUES (4, 'galaxy_A4', 'dydyclon', false, true, 6.00, 156, 230);
INSERT INTO public.galaxy VALUES (5, 'galaxy_A5', 'eilon', false, true, 5.00, 150, 223);
INSERT INTO public.galaxy VALUES (6, 'galaxy_A6', 'fiflemon', true, false, 4.00, 151, 123);
INSERT INTO public.galaxy VALUES (7, 'galaxy_A7', 'heylon', true, true, 3.00, 150, 124);
INSERT INTO public.galaxy VALUES (8, 'gala_tiron', NULL, true, true, NULL, NULL, 2);
INSERT INTO public.galaxy VALUES (9, 'gala_man', NULL, false, true, NULL, NULL, 20);
INSERT INTO public.galaxy VALUES (10, 'galamonta', NULL, true, false, NULL, NULL, 26);
INSERT INTO public.galaxy VALUES (11, 'galanine', NULL, false, false, NULL, NULL, 30);
INSERT INTO public.galaxy VALUES (12, 'predicton', NULL, false, true, NULL, NULL, 25);
INSERT INTO public.galaxy VALUES (13, 'galaxy_A13', 'galcone', true, false, 5.00, 120, 14);
INSERT INTO public.galaxy VALUES (14, 'galaxy_A14', 'cylcine', false, true, 5.50, 121, 15);
INSERT INTO public.galaxy VALUES (15, 'galaxy_A15', 'dyrone', false, true, 5.60, 122, 16);
INSERT INTO public.galaxy VALUES (16, 'galaxy_A16', 'dairyne', true, false, 5.70, 123, 17);
INSERT INTO public.galaxy VALUES (17, 'galaxy_A17', 'dauone', false, false, 5.80, 124, 18);
INSERT INTO public.galaxy VALUES (18, 'galaxy_A18', 'bayrone', true, true, 1.00, 126, 19);
INSERT INTO public.galaxy VALUES (19, 'galaxy_A19', 'bleuestone', true, true, 2.00, 102, 20);
INSERT INTO public.galaxy VALUES (20, 'galaxy_A20', 'babaline', false, false, 2.20, 103, 21);


--
-- Data for Name: moon; Type: TABLE DATA; Schema: public; Owner: freecodecamp
--

INSERT INTO public.moon VALUES (1, 'moon_A1', 'times', true, false, 1.00, 1, 55);
INSERT INTO public.moon VALUES (2, 'moon_A3', 'callu', false, true, 2.00, 2, 57);
INSERT INTO public.moon VALUES (3, 'moon_A4', 'moodart', false, false, 3.00, 3, 58);
INSERT INTO public.moon VALUES (4, 'mooon_A5', ' dakrmoon', true, true, 5.00, 4, 145);
INSERT INTO public.moon VALUES (5, 'moon_A6', 'matmoon', false, false, 6.00, 5, 140);
INSERT INTO public.moon VALUES (6, 'moon_A7', 'bitmoon', false, true, 7.00, 6, 124);
INSERT INTO public.moon VALUES (7, 'moon_A8', 'vamoon', true, true, 8.00, 7, 120);
INSERT INTO public.moon VALUES (10, 'moon_A1', 'times', true, false, 10.00, 8, 59);
INSERT INTO public.moon VALUES (11, 'moon_A11', 'times', true, false, 11.00, 9, 505);
INSERT INTO public.moon VALUES (12, 'moon_A12', 'callu1', false, true, 12.00, 10, 507);
INSERT INTO public.moon VALUES (13, 'moon_A13', 'mooda', false, false, 13.00, 11, 508);
INSERT INTO public.moon VALUES (14, 'mooon_A14', ' damoon', true, true, 14.00, 12, 15);
INSERT INTO public.moon VALUES (15, 'moon_A15', 'tmoon', false, false, 15.00, 13, 101);
INSERT INTO public.moon VALUES (16, 'moon_A16', 'toon', false, true, 16.00, 14, 124);
INSERT INTO public.moon VALUES (17, 'moon_A17', 'vmoon', true, true, 17.00, 15, 121);
INSERT INTO public.moon VALUES (18, 'moon_A18', 'times', true, false, 18.00, 16, 115);
INSERT INTO public.moon VALUES (19, 'moon_A19', 'calu1', false, true, 19.00, 17, 517);
INSERT INTO public.moon VALUES (20, 'moon_A20', 'moa', false, false, 20.00, 18, 526);
INSERT INTO public.moon VALUES (21, 'moon_A18', 'times', true, false, 21.00, 19, 1105);
INSERT INTO public.moon VALUES (22, 'moon_A22', 'tims', true, false, 22.00, 20, 15);


--
-- Data for Name: planet; Type: TABLE DATA; Schema: public; Owner: freecodecamp
--

INSERT INTO public.planet VALUES (2, 'venus', 'srbire', false, false, 8, 2, 5);
INSERT INTO public.planet VALUES (3, 'mars', 'lone', true, true, 7, 3, 62);
INSERT INTO public.planet VALUES (4, 'terre', 'terra', false, true, 2, 4, 61);
INSERT INTO public.planet VALUES (5, 'jupiter', 'jeilon', false, true, 5, 5, 60);
INSERT INTO public.planet VALUES (6, 'saturn', 'salemon', true, false, 4, 6, 59);
INSERT INTO public.planet VALUES (7, 'Neptune', 'reyone', true, true, 5, 7, 58);
INSERT INTO public.planet VALUES (1, 'mercure', 'mercyon', false, false, 1, 1, 63);
INSERT INTO public.planet VALUES (8, 'planet_A8', 'times', true, false, 102, 8, 505);
INSERT INTO public.planet VALUES (9, 'moon_A3', 'callu', false, true, 100, 9, 507);
INSERT INTO public.planet VALUES (10, 'moon_A4', 'moodart', false, false, 101, 10, 508);
INSERT INTO public.planet VALUES (11, 'mooon_A5', ' dakrmoon', true, true, 105, 11, 145);
INSERT INTO public.planet VALUES (12, 'mplanet_A6', 'matmoon', false, false, 60, 12, 140);
INSERT INTO public.planet VALUES (13, 'planet_A7', 'bitmoon', false, true, 17, 13, 124);
INSERT INTO public.planet VALUES (14, 'planet_A8', 'vamplan', true, true, 104, 14, 120);
INSERT INTO public.planet VALUES (15, 'moon_A15', 'value', true, false, 18, 15, 115);
INSERT INTO public.planet VALUES (16, 'moon_A17', 'bible', true, false, 19, 16, 116);
INSERT INTO public.planet VALUES (17, 'moon_A17', 'later', false, false, 20, 17, 117);
INSERT INTO public.planet VALUES (18, 'moon_A18', 'biggo', true, true, 21, 18, 118);
INSERT INTO public.planet VALUES (19, 'moon_A19', 'balal', false, false, 22, 19, 119);
INSERT INTO public.planet VALUES (20, 'moon_A21', 'times', true, false, 21, 20, 1015);


--
-- Data for Name: star; Type: TABLE DATA; Schema: public; Owner: freecodecamp
--

INSERT INTO public.star VALUES (2, 'star_A2', 'starbire', false, false, 8.00, 2, 5);
INSERT INTO public.star VALUES (3, 'star_A3', 'starlone', true, true, 7.00, 3, 66);
INSERT INTO public.star VALUES (4, 'star_A4', 'starclon', false, true, 2.00, 4, 20);
INSERT INTO public.star VALUES (5, 'star_A5', 'eilon', false, true, 5.00, 5, 55);
INSERT INTO public.star VALUES (6, 'star_A6', 'starflemon', true, false, 4.00, 6, 56);
INSERT INTO public.star VALUES (7, 'star_A7', 'staryone', true, true, 5.00, 7, 100);
INSERT INTO public.star VALUES (1, 'star_A1', 'aastone', true, false, 9.00, 1, 25);
INSERT INTO public.star VALUES (8, 'star_A8', 'starbike', true, true, 8.00, 8, 11);
INSERT INTO public.star VALUES (9, 'star_A9', 'starlink', true, false, 15.00, 9, 322);
INSERT INTO public.star VALUES (10, 'star_A10', 'staremix', false, true, 25.00, 10, 10);
INSERT INTO public.star VALUES (11, 'star_A11', 'starzone', true, false, 15.00, 11, 65);
INSERT INTO public.star VALUES (12, 'star_12', 'starix', false, true, 24.00, 12, 63);
INSERT INTO public.star VALUES (13, 'star_A13', 'galone', true, false, 5.00, 13, 14);
INSERT INTO public.star VALUES (14, 'star_A14', 'ylcine', false, true, 5.50, 14, 15);
INSERT INTO public.star VALUES (15, 'star_A15', 'dyrone', false, true, 5.60, 15, 16);
INSERT INTO public.star VALUES (16, 'star_A16', 'iryne', true, false, 5.70, 16, 17);
INSERT INTO public.star VALUES (17, 'star_A17', 'uone', false, false, 5.80, 17, 18);
INSERT INTO public.star VALUES (18, 'star_A18', 'yrone', true, true, 1.00, 18, 19);
INSERT INTO public.star VALUES (19, 'star_A19', 'bleune', true, true, 2.00, 19, 26);
INSERT INTO public.star VALUES (20, 'star_A20', 'babaline', false, false, 2.20, 20, 21);


--
-- Data for Name: system; Type: TABLE DATA; Schema: public; Owner: freecodecamp
--

INSERT INTO public.system VALUES (1, 'solar', 1, NULL, NULL, NULL);
INSERT INTO public.system VALUES (2, 'lunar', 2, NULL, NULL, NULL);
INSERT INTO public.system VALUES (3, 'sea', 3, NULL, NULL, NULL);


--
-- Name: galaxy galaxy_galaxy_name_key; Type: CONSTRAINT; Schema: public; Owner: freecodecamp
--

ALTER TABLE ONLY public.galaxy
    ADD CONSTRAINT galaxy_galaxy_name_key UNIQUE (galaxy_name);


--
-- Name: galaxy galaxy_pkey; Type: CONSTRAINT; Schema: public; Owner: freecodecamp
--

ALTER TABLE ONLY public.galaxy
    ADD CONSTRAINT galaxy_pkey PRIMARY KEY (galaxy_id);


--
-- Name: moon moon_character; Type: CONSTRAINT; Schema: public; Owner: freecodecamp
--

ALTER TABLE ONLY public.moon
    ADD CONSTRAINT moon_character UNIQUE (planet_id);


--
-- Name: moon moon_pkey; Type: CONSTRAINT; Schema: public; Owner: freecodecamp
--

ALTER TABLE ONLY public.moon
    ADD CONSTRAINT moon_pkey PRIMARY KEY (moon_id);


--
-- Name: planet planet_pkey; Type: CONSTRAINT; Schema: public; Owner: freecodecamp
--

ALTER TABLE ONLY public.planet
    ADD CONSTRAINT planet_pkey PRIMARY KEY (planet_id);


--
-- Name: planet planet_show; Type: CONSTRAINT; Schema: public; Owner: freecodecamp
--

ALTER TABLE ONLY public.planet
    ADD CONSTRAINT planet_show UNIQUE (planet_show);


--
-- Name: star star_pkey; Type: CONSTRAINT; Schema: public; Owner: freecodecamp
--

ALTER TABLE ONLY public.star
    ADD CONSTRAINT star_pkey PRIMARY KEY (star_id);


--
-- Name: star star_show; Type: CONSTRAINT; Schema: public; Owner: freecodecamp
--

ALTER TABLE ONLY public.star
    ADD CONSTRAINT star_show UNIQUE (star_show);


--
-- Name: system system_pkey; Type: CONSTRAINT; Schema: public; Owner: freecodecamp
--

ALTER TABLE ONLY public.system
    ADD CONSTRAINT system_pkey PRIMARY KEY (system_id);


--
-- Name: system system_sys_show_key; Type: CONSTRAINT; Schema: public; Owner: freecodecamp
--

ALTER TABLE ONLY public.system
    ADD CONSTRAINT system_sys_show_key UNIQUE (sys_show);


--
-- Name: moon moon_moon_character_fkey; Type: FK CONSTRAINT; Schema: public; Owner: freecodecamp
--

ALTER TABLE ONLY public.moon
    ADD CONSTRAINT moon_moon_character_fkey FOREIGN KEY (planet_id) REFERENCES public.planet(planet_id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: planet planet_planet_character_fkey; Type: FK CONSTRAINT; Schema: public; Owner: freecodecamp
--

ALTER TABLE ONLY public.planet
    ADD CONSTRAINT planet_planet_character_fkey FOREIGN KEY (star_id) REFERENCES public.star(star_id) ON DELETE CASCADE;


--
-- Name: star star_star_character_fkey; Type: FK CONSTRAINT; Schema: public; Owner: freecodecamp
--

ALTER TABLE ONLY public.star
    ADD CONSTRAINT star_star_character_fkey FOREIGN KEY (galaxy_id) REFERENCES public.galaxy(galaxy_id);


--
-- PostgreSQL database dump complete
--

