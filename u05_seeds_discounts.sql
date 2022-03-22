--
-- PostgreSQL database dump
--

-- Dumped from database version 14.1 (Debian 14.1-1.pgdg110+1)
-- Dumped by pg_dump version 14.2 (Ubuntu 14.2-1.pgdg21.10+1)

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

--
-- Data for Name: discounts; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.discounts (id, product, discount_percent) FROM stdin;
beaafc78-8d80-4440-930e-f62bb700fe23	eb4d618c-122d-4428-b022-38aa1ad36fe0	13
55e59428-9a5c-4d65-a402-e48e1e22641a	6c944a17-7606-42f4-a045-df459f6a8c6e	9
60b2d4e9-fc53-48be-9b7a-520926352971	19e67404-6e35-45b7-8d6f-e5bc5b79c453	25
\.


--
-- PostgreSQL database dump complete
--

