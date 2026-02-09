1. Get all unique statuses sorted alphabetically

SELECT DISTINCT status
FROM tasks
ORDER BY status;

2. Get number of tasks in each project, sorted by task count descending

SELECT p.id, p.name, COUNT(t.id) AS tasks_count
FROM projects p
LEFT JOIN tasks t ON t.project_id = p.id
GROUP BY p.id, p.name
ORDER BY tasks_count DESC;

3. Get number of tasks in each project, sorted by project name
SELECT p.id, p.name, COUNT(t.id) AS tasks_count
FROM projects p
LEFT JOIN tasks t ON t.project_id = p.id
GROUP BY p.id, p.name
ORDER BY p.name;

4. Get tasks for all projects whose names start with letter "N"
SELECT t.*
FROM tasks t
JOIN projects p ON t.project_id = p.id
WHERE p.name LIKE 'N%';

5. Get list of all projects containing letter "a" in the middle of the name,
showing task count (including projects without tasks and tasks with NULL project_id)

SELECT p.id, p.name, COUNT(t.id) AS tasks_count
FROM projects p
LEFT JOIN tasks t ON t.project_id = p.id
WHERE p.name LIKE '%a%'
GROUP BY p.id, p.name;

6. Get list of tasks with duplicate names, sorted alphabetically

SELECT name
FROM tasks
GROUP BY name
HAVING COUNT(*) > 1
ORDER BY name;

7. Get list of tasks with exact duplicates by name and status
from project "For home", sorted by number of duplicates

SELECT t.name, t.status, COUNT(*) AS duplicates_count
FROM tasks t
JOIN projects p ON t.project_id = p.id
WHERE p.name = 'For home'
GROUP BY t.name, t.status
HAVING COUNT(*) > 1
ORDER BY duplicates_count DESC;

8. Get project names having more than 10 tasks with status "Done",
sorted by project_id

SELECT p.id, p.name
FROM projects p
JOIN tasks t ON t.project_id = p.id
WHERE t.status = 'Выполнено'
GROUP BY p.id, p.name
HAVING COUNT(t.id) > 10
ORDER BY p.id;