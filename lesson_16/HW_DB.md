## Citizens (`citizens`)
| citizen_id | name  | age | address | employment_status | education_level |
| ---------- | ----- | --- | ------- | ----------------- | --------------- |
| 1          | John  | 25  | Kyiv    | Employed          | Bachelor's      |
| 2          | Marry | 22  | Lviv    | Unemployed        | Master's        |
| 3          | Mark  | 70  | Dnipro  | Retired           | High School     |

## Public Services (`public_services`)
| service_id | service_name          | description             | department           |
| ---------- | --------------------- | ----------------------- | -------------------- |
| 1          | Healthcare            | General health services | Health Department    |
| 2          | Education             | Public school access    | Education Department |
| 3          | Unemployment Benefits | Financial aid           | Labor Department     |

## Service Usage (`service_usage`)
| usage_id | citizen_id | service_id | usage_date | usage_frequency |
| -------- | ---------- | ---------- | ---------- | --------------- |
| 1        | 1          | 1          | 2024-01-15 | Monthly         |
| 2        | 2          | 2          | 2024-02-10 | Once            |
| 3        | 1          | 3          | 2024-03-05 | Annually        |

## Infrastructure (`infrastucture`)
| infrastructure_id | type     | name             | location  | built_year | last_maintenance | managed_by |
| ----------------- | -------- | ---------------- | --------- | ---------- | ---------------- | ---------- |
| 1                 | Road     | Main St Highway  | Kyiv      | 2000       | 2024-06-01       | 1          |
| 2                 | School   | Central High     | Lviv      | 1995       | 2023-12-15       | 2          |
| 3                 | Hospital | General Hospital | Kyiv      | 2010       | 2024-03-10       | 1          |

## Social Programs (`social_programs`)
| program_id | program_name       | description       | start_date | end_date   | budget     |
| ---------- | ------------------ | ----------------- | ---------- | ---------- | ---------- |
| 1          | Housing Assistance | Housing support   | 2020-01-01 | 2030-01-01 | 10,000,000 |
| 2          | Scholarships       | Education funding | 2018-09-01 | 2028-09-01 | 5,000,000  |

## Program Enrollment (`program_enrolment`)
| enrollment_id | citizen_id | program_id | enrollment_date | status    |
| ------------- | ---------- | ---------- | --------------- | --------- |
| 1             | 1          | 1          | 2022-05-10      | Active    |
| 2             | 2          | 2          | 2021-08-15      | Completed |

## Government Employees (`gov_employees`)
| employee_id | first_name | last_name | position            | department           | phone        |
| ----------- | ---------- | --------- | ------------------- | -------------------- | ------------ |
| 1           | Alice      | Brown     | Infrastructure Lead | Public Works         | 380971234567 |
| 2           | Bob        | White     | Education Manager   | Education Department | 380999876543 |


# Relations:

- `service_usage.citizen_id` → `citizens.citizen_id`

- `service_usage.service_id` → `public_services.service_id`

- `program_enrollment.citizen_id` → `citizens.citizen_id`

- `program_enrollment.program_id` → `social_programs.program_id`

- `infrastructure.managed_by`→ `gov_employees.employee_id`