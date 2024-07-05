create database floatv;
use floatv;

Create table man (idm int primary key auto_increment, lastname varchar(15), firstname varchar(15), otc varchar(15), passport varchar(25) unique, datebirth date);

Create table floatm (idf int primary key auto_increment, address varchar(30), area int, price decimal(12, 2), id_m int, foreign key (id_m) references man (idm));

Create table Nalog (idn int primary key auto_increment, daten date, pricen decimal(4, 2), Stavka int, id_f int, foreign key (id_f) references floatm (idf)); 

Create table nalog_year (idny int primary key auto_increment, dateny date, total_price decimal(12, 2), id_f int, foreign key (id_f) references floatm (idf));

-- представление, которое выводит количество квартир, кадастровая стоимость которых между 2000000 и 2500000 площадью более 40 кв.м
create view v1 as select
count(idf) from floatm
where area > 40 and price > 2000000.00 and price < 2500000.00;

-- Написать хранимую процедуру с транзакцией, которая запускается при начислении налога наимущество за отчетный год, необходимо делать соответствующую запись о событии в БД
delimiter $$
create procedure p1(in idfloat int)
begin
declare stavkaf int;
select stavka into stavkaf from nalog
where id_f = idfloat;
start transaction;
if stavkaf is null then rollback;
else
insert into nalog_year (dateny, total_price, id_f)
values (now(), stavkaf * 12, idfloat);
commit;
end if;
end $$
delimiter ;
-- Написать триггер, который отслеживает добавление в бд новых объектов недвижимости, производит начисление налога на текущий год, о чем делает запись в соответствующую таблицу
-- Квартира до 1000 000 рублей - ставка 0,1%, 
-- От 1 млн до 2 млн - 0,15 %
-- От 2 до 5 млн - 0,2%
-- Расчет ставки: кадастровая стоимость * налоговую ставку
delimiter $$
create trigger t1 after insert on floatm
for each row
begin
declare sumnalog decimal(4, 2);
if new.price < 1000000 then set sumnalog = 0.1;
elseif new.price >= 1000000 and new.price < 2000000 then set sumnalog = 0.15;
else set sumnalog = 0.2;
end if;
insert into nalog (daten, pricen, stavka, id_f)
values (now(), sumnalog , new.price * sumnalog / 100 , new.idf);
end $$
delimiter ;


