create table employee (
    id int,
    name varchar(10),
    salary int,
    department varchar(20)
);
insert into employee (id, name, salary, department) values
(1, 'a', 10, 'IT'),
(2, 'b', 20, 'HR'),
(3, 'c', 30, 'Finance'),
(4, 'd', 40, 'IT'),
(5, 'e', 50, 'HR'),
(6, 'f', 60, 'Marketing');

--  give me the departments having employees more than HR department count 
select department from employee group by department having count(department)>(select count(department)  from employee where department="HR");

-- Find  Departments whose salary is more than 25
select distinct department  from employee where salary>25; 

-- give me all employees who are having highest salary in a company 
select *from employee where salary=(select max(salary) from employee);

-- employees who are having salary more than average salary of their department
select *from employee e where salary>(select avg(salary) from employee where department=e.department);

-- employees who earn same salary as others
insert into employee values(7, 'g', 60, 'IT');
select *from employee e1 join employee e2 on e1.salary=e2.salary  and e1.id!=e2.id;

-- list of employees from departments with more than 2 employees
select department from employee group by department having count(department)>2;

-- find the second highest salary from employee table
select max(salary) from employee where salary<(select max(salary) from employee);

-- find the departmetns where total salary > total salary of IT department
insert into employee values(8, 'h', 80, 'HR');
select department from employee group by department having sum(salary)>(select sum(salary) from employee where department="IT");





