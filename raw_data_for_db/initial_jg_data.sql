-- SQL script to insert initial data for a single firm, consultant, and project
-- into the new Django model structure.

-- This script is designed to be run once to set up the initial data.

START TRANSACTION;

-- Step 1: Get the ID for the existing Firm
-- We assume 'One South' has already been inserted into the database.
-- This query retrieves its ID to be used in subsequent steps.
SET @firm_id = (SELECT id FROM profiles_firm WHERE firm_name = 'One South' LIMIT 1);

-- Step 2: Insert the Consultant
-- We create the consultant record for James Karanu Gathogo.
INSERT INTO `profiles_consultant` (`name`, `email`, `phone`, `linkedin`)
VALUES ('James Karanu Gathogo', 'james@gathogo.co.ke', '+254720847745', 'https://www.linkedin.com/in/james-gathogo-1665b437');
-- Get the ID of the newly inserted consultant
SET @consultant_id = LAST_INSERT_ID();

-- Step 3: Link the Consultant to the Firm
-- This populates the many-to-many relationship table.
INSERT INTO `profiles_consultant_firms` (`consultant_id`, `firm_id`)
VALUES (@consultant_id, @firm_id);

-- Step 4: Insert the Project
-- This creates the project record, linking it to the 'One South' firm.
-- Data is taken from the 'Skill Up! Impact Evaluation Design' assignment.
INSERT INTO `profiles_project` (`title`, `client`, `start_date`, `end_date`, `project_summary`, `sectors`, `methodologies`, `firm_portfolio_id`)
VALUES (
    'Systems & Evaluation Specialist – Skill Up! Impact Evaluation Design',
    'Welthungerhilfe (WHH)',
    '2025-05-01',
    NULL, -- The project is ongoing ("May 2025 – Present")
    'WHH’s Skill Up! is a flagship program focused on improving the economic resilience of vulnerable youth through technical, business, and transferable skills training. Implemented across 15 countries, the program aims to enhance income, self-employment, and food security outcomes for youth and their families. This assignment supports the design of a robust impact evaluation approach aligned with WHH’s new Skills Development Portfolio and organizational impact standards. The evaluation will cover 6 anglophone countries and assess causal effects of the program on core outcomes under the “resources” pillar.',
    '["Entrepreneurship", "Youth Economic Empowerment", "Livelihoods and Food Security", "Monitoring, Evaluation, Accountability and Learning (MEAL)", "Youth Entrepreneurship"]',
    '["Impact Evaluation", "Tracer Studies", "Theory of Change Review", "Indicator Mapping"]',
    @firm_id
);
-- Get the ID of the newly inserted project
SET @project_id = LAST_INSERT_ID();

-- Step 5: Insert the Consultant's Role on the Project
-- This creates the link between the consultant and the project, describing their specific role.
INSERT INTO `profiles_consultantrole` (`project_id`, `consultant_id`, `role_title`, `role_description`, `tasks`)
VALUES (
    @project_id,
    @consultant_id,
    'Systems & Evaluation Specialist',
    'As Systems and Evaluation Specialist, I co-lead the development of an impact evaluation design and data collection guidelines. My responsibilities include contextualizing MEL systems for feasibility, advising on outcome indicator alignment, and supporting the adaptation of tracer study tools. I contribute to tool development, co-author deliverables including the feasibility brief and inception report, and advise on capacity building and pilot data collection',
    '- Conducted a literature review on causal effect relationships relevant to youth economic empowerment and skills development under WHH’s “resources” outcome area. [Academic databases, WHH documentation, Word]\n- Developed the Outcome Indicator Reference Sheet, reviewing existing WHH indicators and aligning them with key evaluation outcomes. [Excel, WHH ToC documents, KoBoToolbox (referenced)]\n- Led sessions to identify key outcomes of interest under the ''resources'' pillar for impact evaluation, in collaboration with country teams. [Miro, Zoom, Word]\n- Authored the WHH Impact Evaluation Inception Report, detailing methodology, sampling strategy, tools, and timeline for implementation. [Word, Excel, feasibility matrix]\n- Led the piloting of baseline data collection with country teams, testing revised tools and providing guidance during rollout. [Tracer tool, data collection guide, Zoom]'
);

COMMIT;

-- SQL script to add Education, Certifications, Publications, and Languages
-- for an EXISTING consultant.
--
-- This script is safe to run because it looks up the existing consultant
-- instead of trying to create a new one.

START TRANSACTION;

-- Step 1: Get the ID of the existing consultant, James Karanu Gathogo.
-- We use the email address as it is a unique identifier.
SET @consultant_id = (SELECT id FROM profiles_consultant WHERE email = 'james@gathogo.co.ke' LIMIT 1);

-- Step 2: Insert Education records for the consultant
INSERT INTO `profiles_education` (`consultant_id`, `degree`, `institution`, `location`, `start_year`, `end_year`, `field_of_study`, `graduation_status`, `dissertation_title`, `dissertation_link`) VALUES
(@consultant_id, "Master's degree, Information Systems", "University of Nairobi, School of Computing and Informatics", "Nairobi, Kenya", "2011-01-01", "2014-12-31", "Information Systems", "Graduated", "A model for post-implementation evaluation of health information systems: The case of the DHIS 2 in Kenya", "https://erepository.uonbi.ac.ke/bitstream/handle/11295/73090/Gathogo_A%20model%20for%20post-implementation%20evaluation%20of%20health%20information%20systems%3a%20The%20case%20of%20the%20DHIS%202%20in%20Kenya.pdf?sequence=1&isAllowed=y"),
(@consultant_id, "Bachelor's Degree, Economics", "Moi University", "Eldoret, Kenya", "1998-01-01", "2002-12-31", "Economics", "Graduated", NULL, NULL);

-- Step 3: Insert Certification records for the consultant
INSERT INTO `profiles_certification` (`consultant_id`, `certification_name`, `issuer`, `issue_date`, `expiry_date`, `description`, `certification_link`) VALUES
(@consultant_id, "15.071x: The Analytics Edge", "edX", "2015-06-01", NULL, NULL, "https://s3.amazonaws.com/verify.edx.org/downloads/6e39c35be6bf4829a07f5950d872a211/Certificate.pdf"),
(@consultant_id, "Data Analysis and Statistical Inference", "Coursera", "2015-05-01", NULL, NULL, "https://www.coursera.org/account/accomplishments/verify/R47WSQLAJ7"),
(@consultant_id, "Power BI Data Analyst Associate", "Microsoft", "2025-01-10", NULL, "Validated skills in data modelling and dashboards", "https://learn.microsoft.com/api/credentials/share/en-us/JamesGathogo-5472/49F3701A635226F9?sharingId=B077B281789B1B9C"),
(@consultant_id, "Microsoft Certified: Power Platform Fundamentals", "Microsoft", "2024-08-01", NULL, NULL, "https://learn.microsoft.com/en-us/users/jamesgathogo-5472/credentials/82e980aa39a53240"),
(@consultant_id, "Designing and Running Randomized Evaluations", "MITx on edX", "2020-09-01", NULL, NULL, "https://micromasters.mit.edu/certificate/course/d685c34d6453bbfc9a18234914f9ba3f");

-- Step 4: Insert Publication records for the consultant
INSERT INTO `profiles_publication` (`consultant_id`, `title`, `authors`, `year`, `publisher`, `link`) VALUES
(@consultant_id, "Case Study - Advocating for Digital Health Legislation in Kenya", "Gathogo, J., Omarshah, T.", 2025, "Transform Health", "https://transformhealthcoalition.org/wp-content/uploads/2025/04/Advocating-for-Digital-Health-Legislation-in-Kenya.pdf"),
(@consultant_id, "Case Study - Digital Health Curriculum Reform in Indonesia", "Gathogo, J., Omarshah, T.", 2025, "Transform Health", "https://transformhealthcoalition.org/wp-content/uploads/2025/04/Digital-Health-Curriculum-Reform-in-Indonesia.pdf"),
(@consultant_id, "2024 KPI Progress Report on Delivering the Global Strategic Framework (GSF)", "Gathogo, J., One South", 2025, "Amnesty International", "https://drive.google.com/open?id=1pTBi45mg4AujVU_NefIhMFx8nslr7Krq&usp=drive_fs"),
(@consultant_id, "Endline Evaluation of the Umunthu Health Care Workers Project", "Gathogo, J., Navarrete, A.", 2024, "ArtGlo Africa", "https://artgloafrica.org/wp-content/uploads/2024/02/Umunthu-Health-Project-Endline-Report-1.pdf"),
(@consultant_id, "Endline Evaluation Report - Accelerating Youth-Led Businesses in the Digital Era Programme", "Gathogo, J., Bolza-Schünemann, E., Goldstein, E., Navarrete, A.", 2022, "Youth Business International", "https://youthbusiness.org/wp-content/uploads/2023/12/Endline-Evaluation-Report-1.pdf"),
(@consultant_id, "Endline Evaluation Report - GEC-T Inclusive Education in Kenya’s Lake Region", "Omarshah, T., Bolza-Schünemann, E., Gathogo, J.", 2022, "Leonard Cheshire", "https://girlseducationchallenge.org/media/g04mcgkx/lc-kenya_endline-report-web.pdf"),
(@consultant_id, "Final Evaluation of the Road to Growth Kenya Project", "Bolza-Schünemann, E., Gathogo, J., Goldstein, E., Navarrete, A.", 2022, "Cherie Blair Foundation", "https://drive.google.com/file/d/18_9CeT5CfhWPoe__GqXcJ2Q_T3vsPuqO/view?usp=drive_link");

-- Step 5: Insert Language records for the consultant
INSERT INTO `profiles_language` (`consultant_id`, `language`, `level`) VALUES
(@consultant_id, "English", "Fluent"),
(@consultant_id, "Kiswahili", "First language");

COMMIT;

