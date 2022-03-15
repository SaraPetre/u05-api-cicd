--
-- PostgreSQL database dump
--

-- Dumped from database version 14.1 (Debian 14.1-1.pgdg110+1)
-- Dumped by pg_dump version 14.1 (Debian 14.1-1.pgdg110+1)

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
-- Name: discounts; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.discounts (
    id uuid NOT NULL,
    product uuid NOT NULL,
    discount_percent integer NOT NULL
);


ALTER TABLE public.discounts OWNER TO postgres;

--
-- Name: inventory; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.inventory (
    id uuid NOT NULL,
    product uuid NOT NULL,
    quantity integer NOT NULL,
    store uuid NOT NULL
);


ALTER TABLE public.inventory OWNER TO postgres;

--
-- Name: prices; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.prices (
    id uuid NOT NULL,
    product uuid NOT NULL,
    price numeric NOT NULL
);


ALTER TABLE public.prices OWNER TO postgres;

--
-- Name: products; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.products (
    id uuid NOT NULL,
    article_nr integer NOT NULL,
    name character varying(100) NOT NULL,
    description text
);


ALTER TABLE public.products OWNER TO postgres;

--
-- Name: sales; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.sales (
    id uuid NOT NULL,
    "time" timestamp without time zone NOT NULL,
    store uuid NOT NULL
);


ALTER TABLE public.sales OWNER TO postgres;

--
-- Name: sold_products; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.sold_products (
    id uuid NOT NULL,
    product uuid NOT NULL,
    sale uuid NOT NULL,
    quantity integer NOT NULL
);


ALTER TABLE public.sold_products OWNER TO postgres;

--
-- Name: store_addresses; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.store_addresses (
    id uuid NOT NULL,
    store uuid NOT NULL,
    address text NOT NULL,
    zip character varying(6) NOT NULL,
    city character varying(50) NOT NULL
);


ALTER TABLE public.store_addresses OWNER TO postgres;

--
-- Name: stores; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.stores (
    id uuid NOT NULL,
    name character varying(50) NOT NULL
);


ALTER TABLE public.stores OWNER TO postgres;

--
-- Data for Name: discounts; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.discounts (id, product, discount_percent) FROM stdin;
\.


--
-- Data for Name: inventory; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.inventory (id, product, quantity, store) FROM stdin;
\.


--
-- Data for Name: prices; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.prices (id, product, price) FROM stdin;
\.


--
-- Data for Name: products; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.products (id, article_nr, name, description) FROM stdin;
\.


--
-- Data for Name: sales; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.sales (id, "time", store) FROM stdin;
\.


--
-- Data for Name: sold_products; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.sold_products (id, product, sale, quantity) FROM stdin;
\.


--
-- Data for Name: store_addresses; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.store_addresses (id, store, address, zip, city) FROM stdin;
\.


--
-- Data for Name: stores; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.stores (id, name) FROM stdin;
\.


--
-- Name: discounts discounts_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.discounts
    ADD CONSTRAINT discounts_pkey PRIMARY KEY (id);


--
-- Name: discounts discounts_product_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.discounts
    ADD CONSTRAINT discounts_product_key UNIQUE (product);


--
-- Name: inventory inventory_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.inventory
    ADD CONSTRAINT inventory_pkey PRIMARY KEY (id);


--
-- Name: inventory inventory_product_store_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.inventory
    ADD CONSTRAINT inventory_product_store_key UNIQUE (product, store);


--
-- Name: prices prices_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.prices
    ADD CONSTRAINT prices_pkey PRIMARY KEY (id);


--
-- Name: prices prices_product_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.prices
    ADD CONSTRAINT prices_product_key UNIQUE (product);


--
-- Name: products products_article_nr_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.products
    ADD CONSTRAINT products_article_nr_key UNIQUE (article_nr);


--
-- Name: products products_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.products
    ADD CONSTRAINT products_name_key UNIQUE (name);


--
-- Name: products products_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.products
    ADD CONSTRAINT products_pkey PRIMARY KEY (id);


--
-- Name: sales sales_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.sales
    ADD CONSTRAINT sales_pkey PRIMARY KEY (id);


--
-- Name: sold_products sold_products_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.sold_products
    ADD CONSTRAINT sold_products_pkey PRIMARY KEY (id);


--
-- Name: sold_products sold_products_product_sale_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.sold_products
    ADD CONSTRAINT sold_products_product_sale_key UNIQUE (product, sale);


--
-- Name: store_addresses store_addresses_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.store_addresses
    ADD CONSTRAINT store_addresses_pkey PRIMARY KEY (id);


--
-- Name: store_addresses store_addresses_store_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.store_addresses
    ADD CONSTRAINT store_addresses_store_key UNIQUE (store);


--
-- Name: stores stores_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.stores
    ADD CONSTRAINT stores_name_key UNIQUE (name);


--
-- Name: stores stores_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.stores
    ADD CONSTRAINT stores_pkey PRIMARY KEY (id);


--
-- Name: discounts discounts_product_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.discounts
    ADD CONSTRAINT discounts_product_fkey FOREIGN KEY (product) REFERENCES public.products(id);


--
-- Name: inventory inventory_product_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.inventory
    ADD CONSTRAINT inventory_product_fkey FOREIGN KEY (product) REFERENCES public.products(id);


--
-- Name: inventory inventory_store_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.inventory
    ADD CONSTRAINT inventory_store_fkey FOREIGN KEY (store) REFERENCES public.stores(id);


--
-- Name: prices prices_product_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.prices
    ADD CONSTRAINT prices_product_fkey FOREIGN KEY (product) REFERENCES public.products(id);


--
-- Name: sales sales_store_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.sales
    ADD CONSTRAINT sales_store_fkey FOREIGN KEY (store) REFERENCES public.stores(id);


--
-- Name: sold_products sold_products_product_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.sold_products
    ADD CONSTRAINT sold_products_product_fkey FOREIGN KEY (product) REFERENCES public.products(id);


--
-- Name: sold_products sold_products_sale_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.sold_products
    ADD CONSTRAINT sold_products_sale_fkey FOREIGN KEY (sale) REFERENCES public.sales(id);


--
-- Name: store_addresses store_addresses_store_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.store_addresses
    ADD CONSTRAINT store_addresses_store_fkey FOREIGN KEY (store) REFERENCES public.stores(id);


--
-- PostgreSQL database dump complete
--

