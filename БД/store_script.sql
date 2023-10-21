create database store;
use store;

create table User_
(ID_  varchar(255) primary key,
Mail varchar(255) unique,
password_ varchar(255),
role_ varchar(255),
balance int
);

create table products
(ID_P int auto_increment primary key,
Name_ varchar(255),
Price int,
link varchar(255),
picture blob,
Count int
);

create table basket
(ID_B int auto_increment primary key,
User_ID varchar(255),
ID_Prod int,
constraint cs1_fk foreign key (ID_Prod) references products (ID_P) on update cascade on delete cascade,
constraint cs2_fk  foreign key (User_ID) references User_ (ID_) on update cascade on delete cascade
);


alter table products auto_increment =1000;
alter table basket auto_increment =1000;
