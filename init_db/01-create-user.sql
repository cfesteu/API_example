alter session set container=xepdb1;

create user target identified by "ACMflorin1975!"
    default tablespace users
    temporary tablespace temp
    quota unlimited on users;

grant create session, create table, create view, create sequence, create procedure to target;

grant execute on sys.dbms_lock to target;