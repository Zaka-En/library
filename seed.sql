CREATE TABLE IF NOT EXISTS authors (
  id          INT             AUTO_INCREMENT PRIMARY KEY,
  name        VARCHAR(50)     NOT NULL,
  fullname    VARCHAR(100)    NULL,
  biography   TEXT            NULL,
  country     VARCHAR(30)     NOT NULL
);

CREATE TABLE IF NOT EXISTS books (
  id                  INT             AUTO_INCREMENT PRIMARY KEY,
  isbn                VARCHAR(13)     NOT NULL UNIQUE,
  title               VARCHAR(150)    NOT NULL,
  publication_year    INT             NOT NULL,
  pages               INT             NOT NULL,
  author_id           INT             NOT NULL,
  CONSTRAINT fk_books_author FOREIGN KEY (author_id) REFERENCES authors (id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS users (
  id              INT             AUTO_INCREMENT PRIMARY KEY,
  email           VARCHAR(254)    NOT NULL UNIQUE,
  name            VARCHAR(50)     NOT NULL,
  username        VARCHAR(50)     NULL,
  second_name     VARCHAR(50)     NULL,
  street_adress   VARCHAR(255)    NULL,
  city            VARCHAR(50)     NULL,
  province        VARCHAR(50)     NULL,
  zip_code        VARCHAR(5)      NULL,
  about           TEXT            NULL,
  fullname        VARCHAR(100)    NULL,
  password        VARCHAR(255)    NOT NULL,
  rol             VARCHAR(20)     NOT NULL DEFAULT 'user',
  CONSTRAINT check_user_role CHECK (rol IN ('user', 'admin'))
);

CREATE TABLE IF NOT EXISTS reading_states (
  id              INT         AUTO_INCREMENT PRIMARY KEY,
  book_id         INT         NOT NULL,
  user_id         INT         NOT NULL,
  current_page    INT         NOT NULL,
  start_date      DATETIME    NOT NULL DEFAULT CURRENT_TIMESTAMP,
  finish_date     DATETIME    NULL,
  CONSTRAINT fk_reading_states_book FOREIGN KEY (book_id) REFERENCES books (id) ON DELETE CASCADE,
  CONSTRAINT fk_reading_states_user FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS room_bookings (
  id              INT             AUTO_INCREMENT PRIMARY KEY,
  user_id         INT             NOT NULL,
  room_name       VARCHAR(100)    NOT NULL,
  booking_date    DATE            NOT NULL,
  start_time      TIME            NOT NULL,
  end_time        TIME            NOT NULL,
  notes           TEXT            NULL,
  created_at      DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT fk_room_bookings_user FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
);

INSERT INTO authors (id, name, fullname, biography, country) VALUES
(1, 'Orwell',  'George Orwell',     'Eric Arthur Blair, known by his pen name George Orwell, was an English novelist and essayist.', 'United Kingdom'),
(2, 'Tolkien', 'J.R.R. Tolkien',    'John Ronald Reuel Tolkien was an English writer and professor, best known for The Lord of the Rings.', 'United Kingdom'),
(3, 'Pessoa',  'Fernando Pessoa',   'Portuguese poet, writer and literary critic, considered one of the greatest writers of the 20th century.', 'Portugal'),
(4, 'Borges',  'Jorge Luis Borges', 'Argentine short-story writer, essayist and poet, a key figure in Spanish-language literature.', 'Argentina');

INSERT INTO books (id, isbn, title, publication_year, pages, author_id) VALUES
(1, '9780451524935', 'Nineteen Eighty-Four',       1949, 328, 1),
(2, '9780451526342', 'Animal Farm',                1945, 112, 1),
(3, '9780618640157', 'The Fellowship of the Ring', 1954, 479, 2),
(4, '9780618346257', 'The Two Towers',             1954, 415, 2),
(5, '9780143106463', 'The Book of Disquiet',       1982, 544, 3),
(6, '9780142437209', 'Labyrinths',                 1962, 256, 4);

INSERT INTO users (id, email, name, username, second_name, street_adress, city, province, zip_code, about, fullname, password, rol) VALUES
(1, 'admin@biblioteca.com',    'Admin',  'admin',      NULL,    'Calle Mayor 1',        'Valencia', 'Valencia', '46001', 'Administrador del sistema.', 'Admin Sistema',       '$2b$12$KIXaV1P9yNnILpGxEqGCOuQjJ8PZT4gXhEe6mLkf1M5YnKwZ3Yq4y', 'admin'),
(2, 'ana.garcia@example.com',  'Ana',    'anagarcia',  'García','Avenida del Puerto 22','Valencia', 'Valencia', '46023', 'Lectora empedernida.',       'Ana García López',    '$2b$12$KIXaV1P9yNnILpGxEqGCOuQjJ8PZT4gXhEe6mLkf1M5YnKwZ3Yq4y', 'user'),
(3, 'carlos.ruiz@example.com', 'Carlos', 'carlosruiz', 'Ruiz',  'Calle Colón 5, 3ºB',  'Madrid',   'Madrid',   '28001', 'Apasionado de la literatura latinoamericana.', 'Carlos Ruiz Martínez','$2b$12$KIXaV1P9yNnILpGxEqGCOuQjJ8PZT4gXhEe6mLkf1M5YnKwZ3Yq4y', 'user');

INSERT INTO reading_states (id, book_id, user_id, current_page, start_date, finish_date) VALUES
(1, 1, 2, 145, '2025-03-01 09:00:00', NULL),
(2, 2, 2, 112, '2025-02-10 10:30:00', '2025-02-14 22:15:00'),
(3, 6, 3,  88, '2025-03-10 19:00:00', NULL);

CREATE TABLE conference_rooms (
    id INT NOT NULL AUTO_INCREMENT,
    name VARCHAR(50),
    capacity INT NOT NULL,
    price_per_hour DECIMAL(10, 2),
    is_active BOOLEAN,
    PRIMARY KEY (id)
);

CREATE TABLE room_bookings (
  id INT NOT NULL AUTO_INCREMENT,
  user_id INT,
  room_id INT,
  hour INT NOT NULL,
  date DATE,
  attendees_count INT NOT NULL,
  status VARCHAR(10) DEFAULT 'pending',
  PRIMARY KEY (id),
  CONSTRAINT fk_room_bookings_user FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL,
  CONSTRAINT fk_room_bookings_room FOREIGN KEY (room_id) REFERENCES conference_rooms(id),
  CONSTRAINT check_hour_between_9_and_18 CHECK (hour >= 9 AND hour <= 18),
  CONSTRAINT uq_hour_room_date_booking UNIQUE (hour, room_id, date)
);

INSERT INTO conference_rooms (name, capacity, price_per_hour, is_active) VALUES
('Sala Azul', 10, 25.00, TRUE),
('Sala Verde', 20, 40.00, TRUE),
('Sala Roja', 6, 15.00, TRUE);
