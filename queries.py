average_task_duration = """
    select 
        de.first_name, 
        de.last_name, 
        dd.department_id,
        SUM(f.duration_hours) as total_hours_worked
    from
        target.fact_activity f
    join
        target.dim_employee de
    on 
        f.employee_id = de.employee_id
    join
        target.dim_department dd
    on
        f.department_id = dd.department_id
    where 
        f.activity_type_id = 1
    and
        f.employee_id = to_number(:emp_id)
    group by
        trunc(f.start_ts, 'MM'),
        de.first_name,
        de.last_name,
        dd.department_id
"""