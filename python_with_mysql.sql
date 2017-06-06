USE Python_with_MySQL;


ALTER TABLE Users
MODIFY hashed_password VARCHAR(100) not NULL 





CREATE TABLE Users(
    id INT NOT NULL AUTO_INCREMENT,
    email VARCHAR(255) NOT NULL UNIQUE,
    username VARCHAR(255) NOT NULL,
    hashed_password VARCHAR(255) NOT NULL, 
    PRIMARY KEY(id)
);

