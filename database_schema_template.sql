-- Kazi Database Schema Template
-- This file shows the database structure without containing any personal data
-- Use this as a reference for setting up your own database

-- Database: kazi_db

-- Table structure for consultants
CREATE TABLE `profiles_consultant` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL UNIQUE,
  `phone` varchar(50),
  `linkedin` varchar(500),
  `summary_profile` text,
  `created_at` timestamp DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
);

-- Table structure for firms
CREATE TABLE `profiles_firm` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `description` text,
  `approach_summary` text,
  `created_at` timestamp DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
);

-- Table structure for projects
CREATE TABLE `profiles_project` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(500) NOT NULL,
  `client` varchar(255) NOT NULL,
  `start_date` date,
  `end_date` date,
  `project_summary` text,
  `sectors` json,
  `methodologies` json,
  `created_at` timestamp DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
);

-- Table structure for consultant roles (assignments)
CREATE TABLE `profiles_consultantrole` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `consultant_id` int(11) NOT NULL,
  `project_id` int(11) NOT NULL,
  `role_description` text,
  `tasks` text,
  `created_at` timestamp DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  FOREIGN KEY (`consultant_id`) REFERENCES `profiles_consultant`(`id`),
  FOREIGN KEY (`project_id`) REFERENCES `profiles_project`(`id`)
);

-- Table structure for education
CREATE TABLE `profiles_education` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `consultant_id` int(11) NOT NULL,
  `degree` varchar(255) NOT NULL,
  `institution` varchar(255) NOT NULL,
  `location` varchar(255),
  `start_year` date,
  `end_year` date,
  `field_of_study` varchar(255),
  `graduation_status` varchar(50),
  `dissertation_title` text,
  `dissertation_link` varchar(500),
  PRIMARY KEY (`id`),
  FOREIGN KEY (`consultant_id`) REFERENCES `profiles_consultant`(`id`)
);

-- Table structure for certifications
CREATE TABLE `profiles_certification` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `consultant_id` int(11) NOT NULL,
  `certification_name` varchar(255) NOT NULL,
  `issuer` varchar(255) NOT NULL,
  `issue_date` date,
  `expiry_date` date,
  `description` text,
  `certification_link` varchar(500),
  PRIMARY KEY (`id`),
  FOREIGN KEY (`consultant_id`) REFERENCES `profiles_consultant`(`id`)
);

-- Table structure for publications
CREATE TABLE `profiles_publication` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `consultant_id` int(11) NOT NULL,
  `title` varchar(500) NOT NULL,
  `authors` varchar(500),
  `year` int(4),
  `publisher` varchar(255),
  `link` varchar(500),
  PRIMARY KEY (`id`),
  FOREIGN KEY (`consultant_id`) REFERENCES `profiles_consultant`(`id`)
);

-- Table structure for languages
CREATE TABLE `profiles_language` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `consultant_id` int(11) NOT NULL,
  `language` varchar(100) NOT NULL,
  `level` varchar(50),
  PRIMARY KEY (`id`),
  FOREIGN KEY (`consultant_id`) REFERENCES `profiles_consultant`(`id`)
);

-- Sample data structure (replace with your own data)
INSERT INTO `profiles_consultant` (`name`, `email`, `phone`, `linkedin`, `summary_profile`) VALUES
('[YOUR_NAME]', '[YOUR_EMAIL]', '[YOUR_PHONE]', '[YOUR_LINKEDIN_URL]', '[YOUR_SUMMARY_PROFILE]');

-- Add indexes for better performance
CREATE INDEX idx_consultant_email ON profiles_consultant(email);
CREATE INDEX idx_project_client ON profiles_project(client);
CREATE INDEX idx_consultantrole_consultant ON profiles_consultantrole(consultant_id);
CREATE INDEX idx_consultantrole_project ON profiles_consultantrole(project_id); 