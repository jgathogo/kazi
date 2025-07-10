-- SQL script to insert the 'One South' firm data into your Django-managed database.
--
-- How to use:
-- 1. Connect to your MySQL server using a client (like MySQL Workbench, DBeaver, or the command line).
-- 2. Select your database with the command: USE kazi_db;
-- 3. Copy and paste the entire INSERT statement below and execute it.
--
-- Note: The table name is `profiles_firm` because Django automatically names tables
-- as `appname_modelname`.

INSERT INTO `profiles_firm` (
    `firm_name`,
    `tagline`,
    `founded_year`,
    `email`,
    `website`,
    `phone`,
    `address`,
    `vision`,
    `mission`,
    `approach_summary`,
    `services_offered`,
    `core_expertise`,
    `methodologies`,
    `key_statistics`,
    `thematic_sectors`,
    `donor_experience`,
    `geographical_reach`,
    `quality_assurance_statement`,
    `ethical_commitment_statement`,
    `sustainability_statement`
) VALUES (
    'One South',
    'An international development consulting firm that focuses on understanding and delivering social change.',
    2014,
    'management@one-south.org',
    'https://www.one-south.org',
    NULL, -- Phone number was not provided
    'Wilmington, Delaware, USA',
    'A world where social change is experimental, incremental, and driven by a shared experience.',
    'To support decision-makers in the global south to design relevant programs and deliver impactful social programs through applied research. One South studies the strategic choices and results of development interventions, accumulating knowledge about best practices, identifying emerging trends, and providing informative insights in accessible formats.',
    'One South believes that localizing research for development ensures sustainable results. The firm works closely with in-country partners, bringing together local and global experts to deliver contextualized advice. This approach emphasizes participatory methods, co-designing systems, and fostering shared ownership among stakeholders. Research is typically mixed-methods by design and aims to raise the voices of the most marginalized.',
    '["Planning", "Monitoring", "Evaluation", "Remote Support", "Capacity Building"]',
    '["Monitoring, Evaluation & Learning (MEL)", "Gender and Social Inclusion", "User-centered design for data visualizations", "Sensemaking facilitation", "Sustainability and Adaptability"]',
    '["Contribution Analysis", "Outcome Harvesting", "Most Significant Change", "Process Tracing", "Quasi-experimental designs", "Experimental designs (RCTs)", "Difference-in-difference"]',
    '{"donor_funding_evaluated_usd": 140000000, "countries_of_operation": 40, "local_professionals_trained": 350}',
    '["Education", "Health", "Human Rights", "Disability Inclusion", "Sexual and Reproductive Health", "Economic Empowerment", "Private Sector Development"]',
    '["Global Affairs Canada", "US Department of State", "UK Foreign and Commonwealth Office", "The European Commission", "Irish AID", "The World Bank", "UNESCO", "Various Foundations"]',
    '["Africa", "Asia", "Latin America", "The Middle East", "Eastern Europe", "Central Asia", "The Caribbean"]',
    'One South ensures quality assurance across all deliverables by providing ongoing support for evaluation system design, data analysis, and report generation. Our culturally-competent and rigorous mixed-methods research designs are always aligned with the project''s scope, timeline, and available resources to guarantee the highest quality outputs.',
    'One South is committed to ethical and child-friendly research. We ensure accessibility, rigor, relevance, targeted approaches, and inclusivity in all our work. We protect the autonomy of research participants and employ culturally-competent and age-friendly methods.',
    'We build for sustainability and adaptability, ensuring clients have full ownership of the process and are empowered for long-term independence. We believe that localizing research and enhancing in-country capacity supports the long-term sustainability of development outcomes and fosters a culture of evidence-informed decision-making.'
);
