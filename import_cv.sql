-- SQL script to insert data from master_cv.json

-- Start transaction
START TRANSACTION;

-- Insert Consultant
INSERT INTO `profiles_consultant` (`name`, `email`, `phone`, `linkedin`) VALUES
('James Karanu Gathogo', 'james@gathogo.co.ke', '+254720847745', 'https://www.linkedin.com/in/james-gathogo-1665b437');

-- Get the ID of the inserted consultant
SET @consultant_id = LAST_INSERT_ID();

-- Insert Education
INSERT INTO `profiles_education` (`consultant_id`, `degree`, `institution`, `location`, `start_year`, `end_year`, `field_of_study`, `graduation_status`, `dissertation_title`, `dissertation_link`) VALUES
(@consultant_id, "Master's degree, Information Systems", "University of Nairobi, School of Computing and Informatics", "Nairobi, Kenya", "2011-01-01", "2014-12-31", "Information Systems", "Graduated", "A model for post-implementation evaluation of health information systems: The case of the DHIS 2 in Kenya", "https://erepository.uonbi.ac.ke/bitstream/handle/11295/73090/Gathogo_A%20model%20for%20post-implementation%20evaluation%20of%20health%20information%20systems%3a%20The%20case%20of%20the%20DHIS%202%20in%20Kenya.pdf?sequence=1&isAllowed=y"),
(@consultant_id, "Bachelor's Degree, Economics", "Moi University", "Eldoret, Kenya", "1998-01-01", "2002-12-31", "Economics", "Graduated", NULL, NULL);

-- Insert Certifications
INSERT INTO `profiles_certification` (`consultant_id`, `certification_name`, `issuer`, `issue_date`, `expiry_date`, `description`, `certification_link`) VALUES
(@consultant_id, "15.071x: The Analytics Edge", "edX", "2015-06-01", NULL, NULL, "https://s3.amazonaws.com/verify.edx.org/downloads/6e39c35be6bf4829a07f5950d872a211/Certificate.pdf"),
(@consultant_id, "Data Analysis and Statistical Inference", "Coursera", "2015-05-01", NULL, NULL, "https://www.coursera.org/account/accomplishments/verify/R47WSQLAJ7"),
(@consultant_id, "Power BI Data Analyst Associate", "Microsoft", "2025-01-10", NULL, "Validated skills in data modelling and dashboards", "https://learn.microsoft.com/api/credentials/share/en-us/JamesGathogo-5472/49F3701A635226F9?sharingId=B077B281789B1B9C"),
(@consultant_id, "Microsoft Certified: Power Platform Fundamentals", "Microsoft", "2024-08-01", NULL, NULL, "https://learn.microsoft.com/en-us/users/jamesgathogo-5472/credentials/82e980aa39a53240"),
(@consultant_id, "Designing and Running Randomized Evaluations", "MITx on edX", "2020-09-01", NULL, NULL, "https://micromasters.mit.edu/certificate/course/d685c34d6453bbfc9a18234914f9ba3f");

-- Insert Assignments
INSERT INTO `profiles_assignment` (`consultant_id`, `title`, `organization`, `location`, `date_range`, `start_date`, `description`, `project_summary`, `role_summary`, `tasks`, `sectors`, `methodologies`) VALUES
(@consultant_id, "Systems & Evaluation Specialist – Skill Up!Impact Evaluation Design", "Welthungerhilfe (WHH)", "Remote / Multi-country (Anglophone Skill Up! countries)", "May 2025 – Present", "2025-05-01", "This assignment involves designing a rigorous and context-appropriate impact evaluation for WHH’s Skill Up! programme, with a focus on assessing the causal effects of youth skills development interventions in six anglophone countries. The consultancy includes the development of methodological guidance, review and alignment of outcome indicators, assessment of feasibility for various impact designs, and delivery of technical documents such as a feasibility brief, inception report, and data collection guidelines to support WHH in conducting a high-quality evaluation", "WHH’s Skill Up! is a flagship program focused on improving the economic resilience of vulnerable youth through technical, business, and transferable skills training. Implemented across 15 countries, the program aims to enhance income, self-employment, and food security outcomes for youth and their families. This assignment supports the design of a robust impact evaluation approach aligned with WHH’s new Skills Development Portfolio and organizational impact standards. The evaluation will cover 6 anglophone countries and assess causal effects of the program on core outcomes under the “resources” pillar.", "As Systems and Evaluation Specialist, I co-lead the development of an impact evaluation design and data collection guidelines. My responsibilities include contextualizing MEL systems for feasibility, advising on outcome indicator alignment, and supporting the adaptation of tracer study tools. I contribute to tool development, co-author deliverables including the feasibility brief and inception report, and advise on capacity building and pilot data collection", "- Conducted a literature review on causal effect relationships relevant to youth economic empowerment and skills development under WHH’s “resources” outcome area. [Academic databases, WHH documentation, Word]
- Developed the Outcome Indicator Reference Sheet, reviewing existing WHH indicators and aligning them with key evaluation outcomes. [Excel, WHH ToC documents, KoBoToolbox (referenced)]
- Led sessions to identify key outcomes of interest under the 'resources' pillar for impact evaluation, in collaboration with country teams. [Miro, Zoom, Word]
- Authored the WHH Impact Evaluation Inception Report, detailing methodology, sampling strategy, tools, and timeline for implementation. [Word, Excel, feasibility matrix]
- Led the piloting of baseline data collection with country teams, testing revised tools and providing guidance during rollout. [Tracer tool, data collection guide, Zoom]", '["Entrepreneurship", "Youth Economic Empowerment", "Livelihoods and Food Security", "Monitoring, Evaluation, Accountability and Learning (MEAL)", "Youth Entrepreneurship"]', '["Impact Evaluation", "Tracer Studies", "Theory of Change Review", "Indicator Mapping"]');

-- Insert Publications
INSERT INTO `profiles_publication` (`consultant_id`, `title`, `authors`, `year`, `publisher`, `link`) VALUES
(@consultant_id, "Case Study - Advocating for Digital Health Legislation in Kenya", "Gathogo, J., Omarshah, T.", 2025, "Transform Health", "https://transformhealthcoalition.org/wp-content/uploads/2025/04/Advocating-for-Digital-Health-Legislation-in-Kenya.pdf"),
(@consultant_id, "Case Study - Digital Health Curriculum Reform in Indonesia", "Gathogo, J., Omarshah, T.", 2025, "Transform Health", "https://transformhealthcoalition.org/wp-content/uploads/2025/04/Digital-Health-Curriculum-Reform-in-Indonesia.pdf"),
(@consultant_id, "2024 KPI Progress Report on Delivering the Global Strategic Framework (GSF)", "Gathogo, J., One South", 2025, "Amnesty International", "https://drive.google.com/open?id=1pTBi45mg4AujVU_NefIhMFx8nslr7Krq&usp=drive_fs"),
(@consultant_id, "Endline Evaluation of the Umunthu Health Care Workers Project", "Gathogo, J., Navarrete, A.", 2024, "ArtGlo Africa", "https://artgloafrica.org/wp-content/uploads/2024/02/Umunthu-Health-Project-Endline-Report-1.pdf"),
(@consultant_id, "Endline Evaluation Report - Accelerating Youth-Led Businesses in the Digital Era Programme", "Gathogo, J., Bolza-Schünemann, E., Goldstein, E., Navarrete, A.", 2022, "Youth Business International", "https://youthbusiness.org/wp-content/uploads/2023/12/Endline-Evaluation-Report-1.pdf"),
(@consultant_id, "Endline Evaluation Report - GEC-T Inclusive Education in Kenya’s Lake Region", "Omarshah, T., Bolza-Schünemann, E., Gathogo, J.", 2022, "Leonard Cheshire", "https://girlseducationchallenge.org/media/g04mcgkx/lc-kenya_endline-report-web.pdf"),
(@consultant_id, "Final Evaluation of the Road to Growth Kenya Project", "Bolza-Schünemann, E., Gathogo, J., Goldstein, E., Navarrete, A.", 2022, "Cherie Blair Foundation", "https://drive.google.com/file/d/18_9CeT5CfhWPoe__GqXcJ2Q_T3vsPuqO/view?usp=drive_link");

-- Insert Languages
INSERT INTO `profiles_language` (`consultant_id`, `language`, `level`) VALUES
(@consultant_id, "English", "Fluent"),
(@consultant_id, "Kiswahili", "First language");

-- Commit transaction
COMMIT;
