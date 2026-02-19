1. Get all unique statuses sorted alphabetically
```sql
SELECT DISTINCT status 
FROM task_scheduler_task 
ORDER BY status ASC;
```
2. Get number of tasks in each project, sorted by task count descending
```sql
SELECT 
    p.name AS project_name, 
    COUNT(t.id) AS tasks_count
FROM task_scheduler_project p
LEFT JOIN task_scheduler_task t ON p.id = t.project_id
GROUP BY p.name
ORDER BY tasks_count DESC;
```

3. Get number of tasks in each project, sorted by project name
```sql
SELECT 
    p.name AS project_name, 
    COUNT(t.id) AS tasks_count
FROM task_scheduler_project p
LEFT JOIN task_scheduler_task t ON p.id = t.project_id
GROUP BY p.name
ORDER BY p.name ASC;
```

4. Get tasks for all projects whose names start with letter "N"
```sql
SELECT t.*
FROM task_scheduler_task t
JOIN task_scheduler_project p ON t.project_id = p.id
WHERE p.name LIKE 'N%';
```

5. Get list of all projects containing letter "a" in the middle of the name,
showing task count (including projects without tasks and tasks with NULL project_id)
```sql
SELECT 
    p.name AS project_name, 
    COUNT(t.id) AS tasks_count
FROM task_scheduler_project p
LEFT JOIN task_scheduler_task t ON p.id = t.project_id
WHERE p.name LIKE '_%a%_'
GROUP BY p.id, p.name;
```

6. Get list of tasks with duplicate names, sorted alphabetically
```sql
SELECT name
FROM task_scheduler_task
GROUP BY name
HAVING COUNT(name) > 1
ORDER BY name ASC;
```
7. Get list of tasks with exact duplicates by name and status
from project "For home", sorted by number of duplicates
```sql
SELECT 
    t.name, 
    t.status, 
    COUNT(*) AS matches_count
FROM task_scheduler_task t
JOIN task_scheduler_project p ON t.project_id = p.id
WHERE p.name = 'Delivery'
GROUP BY t.name, t.status
HAVING COUNT(*) > 1
ORDER BY matches_count DESC;
```
8. Get project names having more than 10 tasks with status "Done",
sorted by project_id
```sql
SELECT 
    p.name
FROM task_scheduler_project p
JOIN task_scheduler_task t ON p.id = t.project_id
WHERE t.status = 'done' 
GROUP BY p.id, p.name
HAVING COUNT(t.id) > 10
ORDER BY p.id ASC;

```