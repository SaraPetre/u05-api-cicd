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
-- Data for Name: products; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.products (id, article_nr, name, description) VALUES ('02d9562f-05e8-49b2-8ace-6e166c440060', 127, 'Kattmat', 'Kattmat av hög kvalité, gjort på 95% råttor och 5% kattgräs.');
INSERT INTO public.products (id, article_nr, name, description) VALUES ('a37c34ae-0895-484a-8b2a-355aea3b6c44', 255, 'Hundmat', 'Bästa maten för din hund. 50% choklad, 50% torkad ödelskinn.');
INSERT INTO public.products (id, article_nr, name, description) VALUES ('eb4d618c-122d-4428-b022-38aa1ad36fe0', 511, 'Elefantkoppel', 'En stilig koppel anpassad till elefant. Justerbar passar elefantnacke mellan 1 och 3 meter i omkrets.');
INSERT INTO public.products (id, article_nr, name, description) VALUES ('6c944a17-7606-42f4-a045-df459f6a8c6e', 1023, 'Sömnpiller och energidryck för djur', 'Jobbar du nattpass hemifrån och vill gärna att ditt husdjur ska hålla samma dygnrytm som dig? Här kommer ett bra kit med sömnpiller och energidryck du kan ge ditt husdjur för att styra dess dygnsrytm. Lätt att dosera ut, med lättanvänt tabell som gör kitet användbar för alla djur, från hamstrar till flodhästar. OBS! Inte lämpligt för ugglor och fiskar.');
INSERT INTO public.products (id, article_nr, name, description) VALUES ('19e67404-6e35-45b7-8d6f-e5bc5b79c453', 2047, 'Kattklonare', 'Skulle du passa polarens katt men råka glömma mata den? Råkat köra över eran katt på väg ut ur garaget med bilen? Frukta ej! Denna nya maskin kommer låta dig lätt och smidigt återskapa en katt på bara några timmar. OBS! Fungerar bara om minst 72.5% av det ursprungliga katten finns kvar. Klonpatroner säljs separat.');


--
-- Data for Name: sales; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.sales (id, "time", store) VALUES ('0188146f-5360-408b-a7c5-3414077ceb59', '2022-01-25 13:52:34', '676df1a1-f1d1-4ac5-9ee3-c58dfe820927');
INSERT INTO public.sales (id, "time", store) VALUES ('726ac398-209d-49df-ab6a-682b7af8abfb', '2022-01-26 15:24:45', '75040436-56de-401b-8919-8d0063ac9dd7');
INSERT INTO public.sales (id, "time", store) VALUES ('602fbf9d-2b4a-4de2-b108-3be3afa372ae', '2022-02-07 09:00:56', 'ff53d831-c2fe-4fe8-9f67-5d69118670f2');
INSERT INTO public.sales (id, "time", store) VALUES ('51071ca1-0179-4e67-8258-89e34b205a1e', '2022-02-27 12:32:46', '676df1a1-f1d1-4ac5-9ee3-c58dfe820927');


--
-- Data for Name: sold_products; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.sold_products (id, product, sale, quantity) VALUES ('d3db208c-19ec-496c-8fab-32cb6827eab3', '6c944a17-7606-42f4-a045-df459f6a8c6e', '0188146f-5360-408b-a7c5-3414077ceb59', 12);
INSERT INTO public.sold_products (id, product, sale, quantity) VALUES ('1fbe1c3e-eda9-4f3e-a38a-45a9d05f033b', 'a37c34ae-0895-484a-8b2a-355aea3b6c44', '0188146f-5360-408b-a7c5-3414077ceb59', 3);
INSERT INTO public.sold_products (id, product, sale, quantity) VALUES ('521dfb0e-1042-43de-8421-fa32c6e0dd8a', 'eb4d618c-122d-4428-b022-38aa1ad36fe0', '726ac398-209d-49df-ab6a-682b7af8abfb', 1);
INSERT INTO public.sold_products (id, product, sale, quantity) VALUES ('2642f1c9-95a2-4e1d-8a80-8bb7dc363051', '02d9562f-05e8-49b2-8ace-6e166c440060', '602fbf9d-2b4a-4de2-b108-3be3afa372ae', 57);
INSERT INTO public.sold_products (id, product, sale, quantity) VALUES ('c0e7e1b7-ce01-44f9-8b19-466970efcf11', '19e67404-6e35-45b7-8d6f-e5bc5b79c453', '51071ca1-0179-4e67-8258-89e34b205a1e', 1);
INSERT INTO public.sold_products (id, product, sale, quantity) VALUES ('6b4605ee-be55-45dd-984c-7a6818b59fb9', '02d9562f-05e8-49b2-8ace-6e166c440060', '51071ca1-0179-4e67-8258-89e34b205a1e', 10);


--
-- PostgreSQL database dump complete
--

