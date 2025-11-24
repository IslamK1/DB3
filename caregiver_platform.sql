-- Create USER table
CREATE TABLE "USER" (
    user_id SERIAL PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    given_name VARCHAR(100) NOT NULL,
    surname VARCHAR(100) NOT NULL,
    city VARCHAR(100),
    phone_number VARCHAR(50),
    profile_description TEXT,
    password VARCHAR(255) NOT NULL
);

-- Create CAREGIVER table
CREATE TABLE CAREGIVER (
    caregiver_user_id INTEGER PRIMARY KEY REFERENCES "USER"(user_id) ON DELETE CASCADE,
    photo VARCHAR(255),
    gender VARCHAR(20),
    caregiving_type VARCHAR(50) NOT NULL CHECK (caregiving_type IN ('babysitter','elderly','playmate')),
    hourly_rate NUMERIC(7,2) NOT NULL CHECK (hourly_rate >= 0),
    biography TEXT
);

-- Create MEMBER table
CREATE TABLE MEMBER (
    member_user_id INTEGER PRIMARY KEY REFERENCES "USER"(user_id) ON DELETE CASCADE,
    house_rules TEXT,
    dependent_description TEXT
);

-- Create ADDRESS table
CREATE TABLE ADDRESS (
    member_user_id INTEGER REFERENCES MEMBER(member_user_id) ON DELETE CASCADE,
    house_number VARCHAR(50),
    street VARCHAR(255),
    town VARCHAR(255),
    PRIMARY KEY (member_user_id, house_number, street)
);

-- Create JOB table
CREATE TABLE JOB (
    job_id SERIAL PRIMARY KEY,
    member_user_id INTEGER REFERENCES MEMBER(member_user_id) ON DELETE CASCADE,
    required_caregiving_type VARCHAR(50) NOT NULL CHECK (required_caregiving_type IN ('babysitter','elderly','playmate')),
    other_requirements TEXT,
    date_posted DATE NOT NULL DEFAULT CURRENT_DATE
);

-- Create JOB_APPLICATION table
CREATE TABLE JOB_APPLICATION (
    caregiver_user_id INTEGER REFERENCES CAREGIVER(caregiver_user_id) ON DELETE CASCADE,
    job_id INTEGER REFERENCES JOB(job_id) ON DELETE CASCADE,
    date_applied DATE NOT NULL DEFAULT CURRENT_DATE,
    PRIMARY KEY (caregiver_user_id, job_id)
);

-- Create APPOINTMENT table
CREATE TABLE APPOINTMENT (
    appointment_id SERIAL PRIMARY KEY,
    caregiver_user_id INTEGER REFERENCES CAREGIVER(caregiver_user_id) ON DELETE SET NULL,
    member_user_id INTEGER REFERENCES MEMBER(member_user_id) ON DELETE SET NULL,
    appointment_date DATE NOT NULL,
    appointment_time TIME NOT NULL,
    work_hours INTEGER NOT NULL CHECK (work_hours > 0),
    status VARCHAR(20) NOT NULL CHECK (status IN ('pending','accepted','declined'))
);


-- Insert at least 10 users


INSERT INTO "USER" (email, given_name, surname, city, phone_number, profile_description, password) VALUES
('arman.armanov@example.com','Arman','Armanov','Astana','+77001234567','Looking for elderly care for father.','pass1'),
('amina.aminova@example.com','Amina','Aminova','Almaty','+77005551234','Mother looking for babysitter.','pass2'),
('dina.issayeva@example.com','Dina','Issayeva','Astana','+77004441234','Family needs occasional playmate.','pass3'),
('bekzat.samatov@example.com','Bekzat','Samatov','Astana','+77003331234','Busy professional, needs nanny.','pass4'),
('gulnar.rahmanova@example.com','Gulnar','Rahmanova','Almaty','+77002221234','Looking for elderly caregiver.','pass5'),
('murat.karimov@example.com','Murat','Karimov','Astana','+77001111234','Experienced caregiver seeking jobs.','pass6'),
('nurgul.zhakypova@example.com','Nurgul','Zhakypova','Shymkent','+77009991234','Playmate for children, creative.','pass7'),
('serik.oglanov@example.com','Serik','Oglanov','Almaty','+77008881234','Babysitter with references.','pass8'),
('alinur.tuleyev@example.com','Alinur','Tuleyev','Astana','+77007771234','Elderly care experience.','pass9'),
('bota.akylbek@example.com','Bota','Akylbek','Astana','+77006661234','Willing to travel between cities.','pass10'),
('extra.user1@example.com','Extra','User1','Kostanay','+77005550001','Test user 1','pass11'),
('extra.user2@example.com','Extra','User2','Astana','+77005550002','Test user 2','pass12');


-- Insert caregivers 

INSERT INTO CAREGIVER (caregiver_user_id, photo, gender, caregiving_type, hourly_rate, biography) VALUES
(6,'/photos/murat.jpg','male','babysitter',8.50,'3 years experience with toddlers.'),
(7,'/photos/nurgul.jpg','female','playmate',7.00,'Art and games based activities.'),
(8,'/photos/serik.jpg','male','babysitter',9.50,'References from 5 families.'),
(9,'/photos/alinur.jpg','male','elderly',12.00,'Trained in elderly care and first aid.'),
(10,'/photos/bota.jpg','female','babysitter',6.50,'Flexible schedule, can travel.'),
(3,'/photos/dina.jpg','female','playmate',5.00,'Student, creative playmate.'),
(5,'/photos/gulnar.jpg','female','elderly',15.00,'Nurse with 10 years experience.'),
(11,'/photos/extra1.jpg','female','babysitter',11.00,'Experienced babysitter.'),
(12,'/photos/extra2.jpg','female','playmate',6.00,'Energetic playmate.'),
(1,'/photos/arman_as_caregiver.jpg','male','elderly',9.00,'Also does caregiving part-time.');


-- Insert members 


INSERT INTO MEMBER (member_user_id, house_rules, dependent_description) VALUES
(1,'No smoking. Keep toys in playroom.','Father, 78, needs help with medication.'),
(2,'No pets. Keep shoes outside.','3-year-old daughter who loves painting.'),
(4,'No loud music after 10pm.','6-year-old son, needs help with homework.'),
(13,'No visitors after 9pm.','Infant, needs feeding and sleep schedule.'), -- note: user 13 doesn't exist -> to avoid FK error, adjust: we'll instead use existing user 3 and 5 etc.
(3,'No pets. Maintain hygiene.','5-year-old boy, likes cars.'),
(5,'No pets. Keep kitchen clean.','Mother needs elderly assistance.'),
(8,'No loud guests.','Baby, needs naps.'),
(2,'No pets. No loud music.','Older parent, needs weekly visits.'),
(4,'No shoes on carpet.','Teenager with special needs.'),
(10,'No smoking.','Aunt, elderly, dementia.');


TRUNCATE MEMBER RESTART IDENTITY CASCADE;

INSERT INTO MEMBER (member_user_id, house_rules, dependent_description) VALUES
(1,'No smoking. Keep toys in playroom.','Father, 78, needs help with medication.'),
(2,'No pets. Keep shoes outside.','3-year-old daughter who loves painting.'),
(4,'No loud music after 10pm.','6-year-old son, needs help with homework.'),
(3,'No pets. Maintain hygiene.','5-year-old boy, likes cars.'),
(5,'No pets. Keep kitchen clean.','Mother needs elderly assistance.'),
(8,'No loud guests.','Baby, needs naps.'),
(10,'No smoking.','Aunt, elderly, dementia.'),
(11,'No pets.','Relative needs daytime company.'),
(12,'Respect sleeping hours.','Toddler, needs daycare.'),
(9,'No shoes on carpet.','Grandparent, needs mobility help.');


-- Insert addresses for members 


INSERT INTO ADDRESS (member_user_id, house_number, street, town) VALUES
(1,'12','Kabanbay Batyr','Astana'),
(2,'45A','Abai Street','Almaty'),
(3,'7','Kabanbay Batyr','Astana'),
(4,'101','Tauke Khan Ave','Astana'),
(5,'22','Zhibek Zholy','Almaty'),
(8,'3B','Pushkin Street','Astana'),
(10,'9','Kabanbay Batyr','Astana'),
(11,'88','Suyunbai Ave','Kostanay'),
(12,'15','Al-Farabi','Almaty'),
(9,'50','Kabanbay Batyr','Astana');

-- Insert jobs 

INSERT INTO JOB (member_user_id, required_caregiving_type, other_requirements, date_posted) VALUES
(2,'babysitter','soft-spoken, patient, 09:00-12:00 weekdays', '2025-11-01'),
(1,'elderly','experience with medication, weekends only', '2025-10-28'),
(4,'babysitter','must have references, 15:00-19:00', '2025-11-10'),
(3,'playmate','creative, likes painting, 12:00-15:00', '2025-11-05'),
(5,'elderly','nurse preferred, no pets', '2025-11-02'),
(8,'babysitter','weekends only, soft-spoken', '2025-11-08'),
(10,'elderly','dementia care experience', '2025-11-03'),
(11,'playmate','art background, 10:00-13:00', '2025-11-07'),
(12,'babysitter','infant care, trained in CPR', '2025-11-09'),
(9,'elderly','must be patient, 09:00-12:00', '2025-11-11');


-- Insert job applications 

INSERT INTO JOB_APPLICATION (caregiver_user_id, job_id, date_applied) VALUES
(6,1,'2025-11-02'),
(8,1,'2025-11-03'),
(3,4,'2025-11-06'),
(7,3,'2025-11-06'),
(9,2,'2025-11-04'),
(10,5,'2025-11-05'),
(11,6,'2025-11-09'),
(12,7,'2025-11-10'),
(1,8,'2025-11-08'),
(5,9,'2025-11-12');


-- Insert appointments 

INSERT INTO APPOINTMENT (caregiver_user_id, member_user_id, appointment_date, appointment_time, work_hours, status) VALUES
(6,1,'2025-11-12','09:00',3,'accepted'),
(8,2,'2025-11-13','10:00',2,'pending'),
(3,4,'2025-11-14','14:00',4,'accepted'),
(7,3,'2025-11-15','11:00',2,'declined'),
(9,5,'2025-11-16','09:30',5,'accepted'),
(10,8,'2025-11-17','08:00',3,'accepted'),
(11,10,'2025-11-18','13:00',2,'pending'),
(1,2,'2025-11-19','10:00',1,'accepted'),
(12,11,'2025-11-20','12:00',2,'accepted'),
(5,9,'2025-11-21','09:00',6,'accepted');


-- 3.1 Update the phone number of Arman Armanov to +77773414141.

UPDATE "USER"
SET phone_number = '+77773414141'
WHERE given_name = 'Arman' AND surname = 'Armanov';

-- 3.2 Add $0.3 commission fee to the Caregivers’ hourly rate if it's less than $10, or 10% if it's not.
UPDATE CAREGIVER
SET hourly_rate = CASE
    WHEN hourly_rate < 10 THEN hourly_rate + 0.30
    ELSE ROUND(hourly_rate * 1.10::numeric, 2)
END;


-- Delete the jobs posted by Amina Aminova.


-- First find Amina's user_id 
DELETE FROM JOB
WHERE member_user_id = (
    SELECT member_user_id FROM MEMBER WHERE member_user_id = 2
);

-- Delete all members who live on Kabanbay Batyr street.
DELETE FROM MEMBER
WHERE member_user_id IN (
    SELECT member_user_id FROM ADDRESS WHERE street = 'Kabanbay Batyr'
);

-- Simple Queries

-- 5.1 Select caregiver and member names for the accepted appointments.


-- caregiver and member names for accepted appointments
SELECT c.caregiver_user_id,
       u1.given_name AS caregiver_given_name,
       u1.surname AS caregiver_surname,
       m.member_user_id,
       u2.given_name AS member_given_name,
       u2.surname AS member_surname,
       a.appointment_date, a.appointment_time, a.work_hours
FROM APPOINTMENT a
JOIN CAREGIVER c ON a.caregiver_user_id = c.caregiver_user_id
JOIN "USER" u1 ON c.caregiver_user_id = u1.user_id
JOIN MEMBER m ON a.member_user_id = m.member_user_id
JOIN "USER" u2 ON m.member_user_id = u2.user_id
WHERE a.status = 'accepted';

-- 5.2 List job ids that contain 'soft-spoken' in their other requirements.
SELECT job_id, other_requirements FROM JOB WHERE other_requirements ILIKE '%soft-spoken%';

-- 5.3 List the work hours of all babysitter positions.
-- Join JOB with APPOINTMENT via member -> appointment
SELECT a.work_hours, j.job_id, j.required_caregiving_type
FROM APPOINTMENT a
JOIN MEMBER m ON a.member_user_id = m.member_user_id
JOIN JOB j ON j.member_user_id = m.member_user_id
WHERE j.required_caregiving_type = 'babysitter';

-- 5.4 List the members who are looking for Elderly Care in Astana and have "No pets." rule.
SELECT u.user_id, u.given_name, u.surname, m.house_rules
FROM MEMBER m
JOIN "USER" u ON m.member_user_id = u.user_id
WHERE (m.dependent_description ILIKE '%elderly%' OR m.dependent_description ILIKE '%Aunt%')
  AND u.city = 'Astana'
  AND m.house_rules ILIKE '%No pets%';


-- Complex Queries
-- 6.1 Count the number of applicants for each job posted by a member (multiple joins with aggregation)


SELECT j.job_id, COUNT(ja.caregiver_user_id) AS applicant_count
FROM JOB j
LEFT JOIN JOB_APPLICATION ja ON j.job_id = ja.job_id
GROUP BY j.job_id
ORDER BY applicant_count DESC;

-- 6.2 Total hours spent by care givers for all accepted appointments (multiple joins with aggregation)
SELECT c.caregiver_user_id, u.given_name, u.surname, SUM(a.work_hours) AS total_hours
FROM APPOINTMENT a
JOIN CAREGIVER c ON a.caregiver_user_id = c.caregiver_user_id
JOIN "USER" u ON c.caregiver_user_id = u.user_id
WHERE a.status = 'accepted'
GROUP BY c.caregiver_user_id, u.given_name, u.surname
ORDER BY total_hours DESC;

-- 6.3 Average pay of caregivers based on accepted appointments (join with aggregation)
SELECT c.caregiver_user_id, u.given_name, u.surname,
       AVG(c.hourly_rate * a.work_hours) AS avg_pay_per_appointment
FROM APPOINTMENT a
JOIN CAREGIVER c ON a.caregiver_user_id = c.caregiver_user_id
JOIN "USER" u ON c.caregiver_user_id = u.user_id
WHERE a.status = 'accepted'
GROUP BY c.caregiver_user_id, u.given_name, u.surname
ORDER BY avg_pay_per_appointment DESC;

-- 6.4 Caregivers who earn above average based on accepted appointments (multiple join with aggregation and nested query)
WITH caregiver_avg AS (
    SELECT c.caregiver_user_id, AVG(c.hourly_rate * a.work_hours) AS avg_earn
    FROM APPOINTMENT a
    JOIN CAREGIVER c ON a.caregiver_user_id = c.caregiver_user_id
    WHERE a.status = 'accepted'
    GROUP BY c.caregiver_user_id
)
SELECT ca.caregiver_user_id, u.given_name, u.surname, ca.avg_earn
FROM caregiver_avg ca
JOIN "USER" u ON ca.caregiver_user_id = u.user_id
WHERE ca.avg_earn > (SELECT AVG(avg_earn) FROM caregiver_avg);


-- Query with a Derived Attribute
-- 7. Calculate the total cost to pay for a caregiver for all accepted appointments.


SELECT c.caregiver_user_id, u.given_name, u.surname,
       SUM(c.hourly_rate * a.work_hours) AS total_cost
FROM APPOINTMENT a
JOIN CAREGIVER c ON a.caregiver_user_id = c.caregiver_user_id
JOIN "USER" u ON c.caregiver_user_id = u.user_id
WHERE a.status = 'accepted'
GROUP BY c.caregiver_user_id, u.given_name, u.surname
ORDER BY total_cost DESC;


-- View Operation
-- 8. View all job applications and the applicants.


CREATE VIEW vw_job_applicants AS
SELECT j.job_id, j.required_caregiving_type, j.other_requirements, j.date_posted,
       c.caregiver_user_id, u.given_name AS caregiver_given_name, u.surname AS caregiver_surname, ja.date_applied
FROM JOB j
LEFT JOIN JOB_APPLICATION ja ON j.job_id = ja.job_id
LEFT JOIN CAREGIVER c ON ja.caregiver_user_id = c.caregiver_user_id
LEFT JOIN "USER" u ON c.caregiver_user_id = u.user_id;

-- Select from view to show contents
SELECT * FROM vw_job_applicants ORDER BY job_id, date_applied;

COMMIT;

