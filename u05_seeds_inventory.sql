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
-- Data for Name: inventory; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.inventory (id, product, quantity, store) FROM stdin;
313affae-16e3-488a-a257-b4ab41d05680	6c944a17-7606-42f4-a045-df459f6a8c6e	73	676df1a1-f1d1-4ac5-9ee3-c58dfe820927
27cd1485-3b10-4b0f-a5f1-b39f6494bbdc	19e67404-6e35-45b7-8d6f-e5bc5b79c453	69	676df1a1-f1d1-4ac5-9ee3-c58dfe820927
18298375-7cb1-4c30-81c8-5a5b80e24a10	02d9562f-05e8-49b2-8ace-6e166c440060	355	676df1a1-f1d1-4ac5-9ee3-c58dfe820927
2a5296ed-9596-42d3-88fc-de5dde0c3294	a37c34ae-0895-484a-8b2a-355aea3b6c44	143	676df1a1-f1d1-4ac5-9ee3-c58dfe820927
93969d8d-862b-4bdd-991b-a588d79e3e87	eb4d618c-122d-4428-b022-38aa1ad36fe0	28	75040436-56de-401b-8919-8d0063ac9dd7
172bb573-4724-431f-aaea-665cef6020d2	02d9562f-05e8-49b2-8ace-6e166c440060	227	ff53d831-c2fe-4fe8-9f67-5d69118670f2
0a4d8a90-d86f-458b-8e04-7183f486b3a9	a37c34ae-0895-484a-8b2a-355aea3b6c44	30	ff53d831-c2fe-4fe8-9f67-5d69118670f2
\.


--
-- PostgreSQL database dump complete
--

