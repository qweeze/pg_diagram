--
-- PostgreSQL database dump
--

-- Dumped from database version 10.9 (Ubuntu 10.9-0ubuntu0.18.04.1)
-- Dumped by pg_dump version 10.9 (Ubuntu 10.9-0ubuntu0.18.04.1)

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
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner:
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner:
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: author; Type: TABLE; Schema: public; Owner: qweeze
--

CREATE TABLE public.author (
    id integer NOT NULL,
    f_name character varying(256) NOT NULL
);


ALTER TABLE public.author OWNER TO qweeze;

--
-- Name: book_author; Type: TABLE; Schema: public; Owner: qweeze
--

CREATE TABLE public.book_author (
    book_id integer,
    author_id integer
);


ALTER TABLE public.book_author OWNER TO qweeze;

--
-- Name: book_genre; Type: TABLE; Schema: public; Owner: qweeze
--

CREATE TABLE public.book_genre (
    book_id integer NOT NULL,
    genre_id integer NOT NULL
);


ALTER TABLE public.book_genre OWNER TO qweeze;

--
-- Name: book_meta; Type: TABLE; Schema: public; Owner: qweeze
--

CREATE TABLE public.book_meta (
    id integer NOT NULL,
    title character varying(1024) NOT NULL,
    f_size integer NOT NULL,
    add_date date,
    lang_id integer,
    origin_id integer NOT NULL
);


ALTER TABLE public.book_meta OWNER TO qweeze;

--
-- Name: book_series; Type: TABLE; Schema: public; Owner: qweeze
--

CREATE TABLE public.book_series (
    book_id integer NOT NULL,
    series_id integer NOT NULL,
    pos integer
);


ALTER TABLE public.book_series OWNER TO qweeze;

--
-- Name: genre; Type: TABLE; Schema: public; Owner: qweeze
--

CREATE TABLE public.genre (
    id integer NOT NULL,
    code character(32) NOT NULL
);


ALTER TABLE public.genre OWNER TO qweeze;

--
-- Name: lang_code; Type: TABLE; Schema: public; Owner: qweeze
--

CREATE TABLE public.lang_code (
    id integer NOT NULL,
    code character(8) NOT NULL
);


ALTER TABLE public.lang_code OWNER TO qweeze;

--
-- Name: series; Type: TABLE; Schema: public; Owner: qweeze
--

CREATE TABLE public.series (
    id integer NOT NULL,
    name character varying(1024) NOT NULL
);


ALTER TABLE public.series OWNER TO qweeze;

--
-- Name: author author_pkey; Type: CONSTRAINT; Schema: public; Owner: qweeze
--

ALTER TABLE ONLY public.author
    ADD CONSTRAINT author_pkey PRIMARY KEY (id);


--
-- Name: book_meta book_meta_pkey; Type: CONSTRAINT; Schema: public; Owner: qweeze
--

ALTER TABLE ONLY public.book_meta
    ADD CONSTRAINT book_meta_pkey PRIMARY KEY (id);


--
-- Name: genre genre_pkey; Type: CONSTRAINT; Schema: public; Owner: qweeze
--

ALTER TABLE ONLY public.genre
    ADD CONSTRAINT genre_pkey PRIMARY KEY (id);


--
-- Name: lang_code lang_code_pkey; Type: CONSTRAINT; Schema: public; Owner: qweeze
--

ALTER TABLE ONLY public.lang_code
    ADD CONSTRAINT lang_code_pkey PRIMARY KEY (id);


--
-- Name: series series_pkey; Type: CONSTRAINT; Schema: public; Owner: qweeze
--

ALTER TABLE ONLY public.series
    ADD CONSTRAINT series_pkey PRIMARY KEY (id);


--
-- Name: genre uq_genre_code; Type: CONSTRAINT; Schema: public; Owner: qweeze
--

ALTER TABLE ONLY public.genre
    ADD CONSTRAINT uq_genre_code UNIQUE (code);


--
-- Name: lang_code uq_lang_code; Type: CONSTRAINT; Schema: public; Owner: qweeze
--

ALTER TABLE ONLY public.lang_code
    ADD CONSTRAINT uq_lang_code UNIQUE (code);


--
-- Name: series uq_series_name; Type: CONSTRAINT; Schema: public; Owner: qweeze
--

ALTER TABLE ONLY public.series
    ADD CONSTRAINT uq_series_name UNIQUE (name);


--
-- Name: book_author autor_fkey_k; Type: FK CONSTRAINT; Schema: public; Owner: qweeze
--

ALTER TABLE ONLY public.book_author
    ADD CONSTRAINT autor_fkey_k FOREIGN KEY (author_id) REFERENCES public.author(id);


--
-- Name: book_author book_fkey_k; Type: FK CONSTRAINT; Schema: public; Owner: qweeze
--

ALTER TABLE ONLY public.book_author
    ADD CONSTRAINT book_fkey_k FOREIGN KEY (book_id) REFERENCES public.book_meta(id);


--
-- Name: book_genre fk_book_genre_book; Type: FK CONSTRAINT; Schema: public; Owner: qweeze
--

ALTER TABLE ONLY public.book_genre
    ADD CONSTRAINT fk_book_genre_book FOREIGN KEY (book_id) REFERENCES public.book_meta(id);


--
-- Name: book_genre fk_book_genre_genre; Type: FK CONSTRAINT; Schema: public; Owner: qweeze
--

ALTER TABLE ONLY public.book_genre
    ADD CONSTRAINT fk_book_genre_genre FOREIGN KEY (genre_id) REFERENCES public.genre(id);


--
-- Name: book_meta fk_book_meta_lang; Type: FK CONSTRAINT; Schema: public; Owner: qweeze
--

ALTER TABLE ONLY public.book_meta
    ADD CONSTRAINT fk_book_meta_lang FOREIGN KEY (lang_id) REFERENCES public.lang_code(id);


--
-- Name: book_series series2_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: qweeze
--

ALTER TABLE ONLY public.book_series
    ADD CONSTRAINT series2_id_fkey FOREIGN KEY (series_id) REFERENCES public.series(id);


--
-- Name: book_series series_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: qweeze
--

ALTER TABLE ONLY public.book_series
    ADD CONSTRAINT series_id_fkey FOREIGN KEY (book_id) REFERENCES public.book_meta(id);


--
-- PostgreSQL database dump complete
--
