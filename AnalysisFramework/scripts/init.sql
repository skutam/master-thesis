DROP DATABASE master_thesis;                            -- Drop database when exist

CREATE DATABASE master_thesis;                          -- Create a new database

USE master_thesis;                                      -- Select database

CREATE TABLE passwords (
    password VARCHAR(256) PRIMARY KEY NOT NULL, 	    -- Password we are saving to database
    `count` INT DEFAULT 1,                      	    -- Number of passwords
    dataset INT DEFAULT 0,                      	    -- Each bit represent one dataset
    tool_generated_dataset INT default 0,       	    -- Each bit will represent combination of Tool and dataset
    gen_count INT DEFAULT 1,							-- Number of passwords in the weak dataset
    total_count INT DEFAULT 0                           -- Total number of passwords, used for indexing
);

CREATE INDEX total_count_index ON passwords (total_count);  -- Index for quicker indexing of passwords by total count

-- After inserting all the passwords run following command
-- UPDATE passwords SET total_count=`count` + gen_count;