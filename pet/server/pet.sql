create database pets;
use pets;

create table category (
idcategory int primary key auto_increment,
namecategory varchar(15) unique);

create table breed (
idbreed int primary key auto_increment,
namebreed varchar(15) unique,
categoryid int,
foreign key (categoryid) references category (idcategory));

create table pet (
idpet int primary key auto_increment,
namepet varchar(15),
breedid int,
color varchar(10),
age int,
availability int,
foreign key (breedid) references breed (idbreed));

create table client (
idclient int primary key auto_increment,
login varchar(15) unique);

create table sale (
idsale int primary key auto_increment,
date_sale datetime,
satussale varchar(10),
clientid int,
petid int,
foreign key (clientid) references client (idclient),
foreign key (petid) references pet (idpet));

create table sold (
idsold int primary key auto_increment,
datesold datetime,
saleid int,
foreign key (saleid) references sale (idsale));

-- представление, которое выводит всех 
-- питомцев по категориям, которые 
-- есть в наличии в магазине (не проданы). 
create view v1 as
select p.namepet, p.age, p.color,
b.namebreed, 
c.namecategory
from pet p 
join breed b ON p.breedid = b.idbreed 
join category c ON b.categoryid = c.idcategory 
where p.availability = 1;




-- хранимая процедура с транзакцией, которая 
-- запускается в момент оформления продажи питомцы, 
-- и делает соответствующую запись о событии в БД, 
-- первоначально доставке присваивается статус «в пути»
delimiter //
create procedure p1 (in idc int, in idp int)
begin
declare avail int;
select availability into avail from pet where idpet = idp;
start transaction;
if avail = 0 then 
rollback;
else
insert into sale (date_sale, satussale, clientid, petid)
values (now(), 'в пути', idc, idp);
end if;
commit;
end //




-- триггер, который отслеживает изменение статуса 
-- доставки на «получен» и ведет логирование данного события 
-- в отдельную таблицу с указанием даты и времени
delimiter //
create trigger t1 after update on sale
for each row
begin
if old.satussale <> new.satussale then
insert into sold (datesold, saleid)
values (now(), new.idsale);
end if;
end //
