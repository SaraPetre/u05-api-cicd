BEGIN;

INSERT INTO stores (id, name) VALUES 
    ('dd4cf820-f946-4f38-8492-ca5dfeed0d74','Djurjouren'), 
    ('75040436-56de-401b-8919-8d0063ac9dd7', 'Djuristen'),
    ('ff53d831-c2fe-4fe8-9f67-5d69118670f2', 'Den Lilla Djurbutiken'),
    ('676df1a1-f1d1-4ac5-9ee3-c58dfe820927', 'Den Stora Djurbutiken'),
    ('a04bb312-9738-4db2-a7a5-ed6be9938afd', 'Noahs Djur & Båtaffär');

INSERT INTO store_addresses (id, store, address, zip, city) VALUES
    ('c62fd71a-4490-4ca8-88b2-b1f808c30368', 
     'dd4cf820-f946-4f38-8492-ca5dfeed0d74',
     'Upplandsgatan 99', '12345', 'Stockholm'), 
    ('e16e4cbc-184c-4e0c-8951-9b851a2f566c',
     '75040436-56de-401b-8919-8d0063ac9dd7',
     'Skånegatan 420', '54321', 'Falun'),
    ('70cf14d8-6bc2-4060-ae36-e6e22b74309f',
     'ff53d831-c2fe-4fe8-9f67-5d69118670f2',
     'Nätverksgatan 22', '55555', 'Hudiksvall'),
    ('008b1b7b-bd10-4c9d-86c1-4966e17d9fdd',
     '676df1a1-f1d1-4ac5-9ee3-c58dfe820927',
     'Routergatan 443', '54545', 'Hudiksvall'),
    ('0c1525a1-edf8-4c24-a387-b53c71af7de2',
     'a04bb312-9738-4db2-a7a5-ed6be9938afd',
     'Stallmansgatan 666', '96427', 'Gävle');


COMMIT;
