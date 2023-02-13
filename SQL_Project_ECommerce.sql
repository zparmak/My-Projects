select * from  dbo.e_commerce_data

ALTER TABLE dbo.e_commerce_data ALTER COLUMN Order_Quantity int;
ALTER TABLE dbo.e_commerce_data ALTER COLUMN Sales int;
ALTER TABLE dbo.e_commerce_data ALTER COLUMN Order_Date date;
ALTER TABLE dbo.e_commerce_data ALTER COLUMN Ship_Date date;



--ANALYSING THE DATA--
--1. Find the top 3 customers who have the maximum count of orders.--
--(Maksimum sipari� say�s�na sahip ilk 3 m��teriyi bulun.)--

SELECT TOP (3) Customer_Name, SUM(Order_Quantity) as total_quantity_by_customer 
FROM dbo.e_commerce_data 
GROUP BY Cust_ID, Customer_Name 
ORDER BY SUM(Order_Quantity) DESC;


--2. Find the customer whose order took the maximum time to get shipping.--
--(Sipari�inin kargoya ula�mas� en uzun s�reyi alan m��teriyi bulun.)--
SELECT TOP 1 Customer_Name, DaysTakenForShipping 
FROM dbo.e_commerce_data 
ORDER BY DaysTakenForShipping DESC;
 

--3. Count the total number of unique customers in January and how many of them came back every month over the entire year in 2011.--
--(Ocak ay�ndaki toplam tekil m��teri say�s�n� ve 2011 y�l� boyunca her ay ka� tanesinin geri geldi�ini say�n.)--

---1. query--
with cte as
(
select Cust_ID, DATENAME(m, order_date) AS [month]
from dbo.e_commerce_data 
where cust_ID IN 
(select distinct Cust_ID from dbo.e_commerce_data 
where DATENAME(m, order_date) = 'January' and year(Order_Date) = 2011)
)

select Cust_ID, DATENAME(m, order_date) AS [month]
from dbo.e_commerce_data 
where cust_ID IN 
(select distinct Cust_ID from dbo.e_commerce_data 
where DATENAME(m, order_date) = 'January' and year(Order_Date) = 2011)

Except

select Cust_ID, DATENAME(m, order_date) AS [month]
from dbo.e_commerce_data where DATENAME(m, order_date) = 'January'

---2. query-- PIVOT ile aylara g�re sayd�rmak istedim. 
select * from (

with cte as
(
select Cust_ID, DATENAME(m, order_date) AS [month]
from dbo.e_commerce_data 
where cust_ID IN 
(select distinct Cust_ID from dbo.e_commerce_data 
where DATENAME(m, order_date) = 'January' and year(Order_Date) = 2011)
)

select Cust_ID, DATENAME(m, order_date) AS [month]
from dbo.e_commerce_data 
where cust_ID IN 
(select distinct Cust_ID from dbo.e_commerce_data 
where DATENAME(m, order_date) = 'January' and year(Order_Date) = 2011)

Except

select Cust_ID, DATENAME(m, order_date) AS [month]
from dbo.e_commerce_data where DATENAME(m, order_date) = 'January'

PIVOT (
count([month])
FOR [Month] IN ([February], [March], [April], [May], [June], 
	[July], [August], [September], [October], [November], [December])

) AS pvt
---
--3. query--
select month(Order_Date) [Month], datename(month, Order_Date) [Month_name], count(distinct Cust_ID) cust_count
from dbo.e_commerce_data where Cust_ID
in (
	select distinct Cust_ID
	from dbo.e_commerce_data
	where month(Order_Date) = 1 and year(Order_date) = 2011
)
and year(Order_date) = 2011
 group by month(Order_Date), DATENAME(MONTH, Order_Date)
 order by [Month]

--4. Write a query to return for each user the time elapsed between the first purchasing and the third purchasing, in ascending order by Customer ID.--
--( Her kullan�c� i�in ilk sat�n alma ile ���nc� sat�n alma aras�nda ge�en s�reyi M��teri Kimli�ine g�re artan s�rada d�nd�rmek i�in bir sorgu yaz�n.)--
with cte as
(
select Cust_ID, Customer_name, order_date, lead(Order_Date, 2) OVER(PARTITION BY Cust_ID Order BY Order_Date ASC) as third_purchasing 
from dbo.e_commerce_data
)
select *, datediff(d, order_date, third_purchasing) AS elapsed_time from cte order by Cust_ID ASC;



--5. Write a query that returns customers who purchased both product 11 and product 14, as well as the ratio of these products to 
--the total number of products purchased by the customer.--
--(Hem 11. hem de 14. �r�n� sat�n alan m��terileri ve bu �r�nlerin m��terinin sat�n ald��� 
--toplam �r�n say�s�na oran�n� d�nd�ren bir sorgu yaz�n.)

--1.query trying--
select t2.Cust_ID, Customer_Name, t1.Order_Quantity/t2.total_quantity from t1, t2
-----
with t1 as
(
select Cust_ID, Customer_Name, Order_Quantity, Prod_ID from dbo.e_commerce_data where Cust_ID IN(

select Cust_ID from dbo.e_commerce_data where Prod_Id = 'Prod_11'
intersect
select Cust_ID from dbo.e_commerce_data where Prod_Id = 'Prod_14'
)),
t2 as
(
select Cust_ID, sum(order_quantity) AS total_all_quantity from dbo.e_commerce_data group by Cust_ID 
),
t3 as
(
select Cust_ID, sum(order_quantity) total_quantity from t1 group by Cust_ID
)
select *, 1.0*(total_quantity / total_all_quantity) AS Return_Rate from t2 join t3 on t2.Cust_ID = t3.Cust_ID

--2. query trying--
select distinct convert(int, SUBSTRING(Cust_ID, 6, len(Cust_ID))) AS Customer_ID,
		CAST (1.0*sum(case when Prod_ID = 'Prod_11' then Order_Quantity else 0  end)/sum(Order_Quantity) AS NUMERIC (3,2)) AS Ratio_P11,
		CAST (1.0*sum(case when Prod_ID = 'Prod_14' then Order_Quantity else 0  end)/sum(Order_Quantity) AS NUMERIC (3,2)) AS Ratio_P14
		
	from dbo.e_commerce_data
	group by Cust_ID
	HAVING
		SUM (CASE WHEN Prod_ID = 'Prod_11' THEN Order_Quantity ELSE 0 END) >= 1 AND
		SUM (CASE WHEN Prod_ID = 'Prod_14' THEN Order_Quantity ELSE 0 END) >= 1



--CUSTOMER SEGMENTATION--
-- 1. Create a �view� that keeps visit logs of customers on a monthly basis. (For each log, three field is kept: Cust_id, Year, Month)
--(M��terilerin ayl�k olarak ziyaret g�nl�klerini tutan bir �g�r�n�m� olu�turun. (Her log i�in �� alan tutulur: Cust_id, Year, Month)--
create view t1 as

select Cust_ID, Year(order_date) As order_year, Datename(m, order_date) as [Months] from dbo.e_commerce_data; 

-- 2. Create a �view� that keeps the number of monthly visits by users. (Show separately all months from the beginning business)
--(Kullan�c�lar�n ayl�k ziyaret say�s�n� tutan bir "g�r�n�m" olu�turun. (�� ba�lang�c�ndan itibaren t�m aylar� ayr� ayr� g�sterin)--


with cte as
(
select Cust_ID, count(ord_ID) As order_count,  year(order_date) As [year],  datename(m, order_date) As [month]
from dbo.e_commerce_data 
group by Cust_ID, datename(m, order_date), year(order_date) 
)
select *, count([month]) over(partition by Cust_ID) as visit_count from cte;


-- 3. For each visit of customers, create the next month of the visit as a separate column.--
--(M��terilerin her ziyareti i�in, ziyaretin bir sonraki ay�n� ayr� bir s�tun olarak olu�turun.)--

select Cust_ID, Customer_name, order_date, month(Order_Date) As [order_month], month(Order_Date)+1 as after_month  
from dbo.e_commerce_data;


-- 4. Calculate the monthly time gap between two consecutive visits by each customer.--
--(Her m��terinin birbirini izleyen iki ziyareti aras�ndaki ayl�k zaman aral���n� hesaplay�n.)--

with cte as
(
select Cust_ID, Customer_name, order_date, lead(Order_Date, 1) OVER(PARTITION BY Cust_ID Order BY Order_Date ASC) as second_purchasing 
from dbo.e_commerce_data
)
select *, datediff(m, order_date, second_purchasing) AS elapsed_time from cte order by Cust_ID ASC;

-- 5. Categorise customers using average time gaps. Choose the most fitted labeling model for you.--
--For example: o Labeled as churn if the customer hasn't made another purchase in the months since they made-- 
--their first purchase. o Labeled as regular if the customer has made a purchase every month. Etc.--
--(Ortalama zaman bo�luklar�n� kullanarak m��terileri kategorilere ay�r�n. Sizin i�in en uygun etiketleme modelini se�in.)--
--�rne�in: o M��teri, ilk sat�n alma i�lemini yapt��� tarihten itibaren aylar i�inde ba�ka bir sat�n alma i�lemi-- 
--ger�ekle�tirmediyse kay�p olarak etiketlenir.
--o M��teri her ay bir sat�n alma i�lemi yapt�ysa, normal olarak etiketlenir.--

with cte as
(
select Cust_ID, Customer_name, order_date, lead(Order_Date, 1) OVER(PARTITION BY Cust_ID Order BY Order_Date ASC) as second_purchasing 
from dbo.e_commerce_data
),
cte2 as
(
select *, datediff(m, order_date, second_purchasing) AS elapsed_time from cte 
)

select *,
	case when elapsed_time <= 3 then 'Regular Customer' 
		when elapsed_time <= 6 then 'Normal Customer' 
		else 'Lossed Customer' END Customer_Category

from cte2


--MONTH-WISE RETENTION RATE--
--1.Find the number of customers retained month-wise. (You can use time gaps)--
--(Ayl�k elde tutulan m��teri say�s�n� bulun. (Zaman bo�luklar�n� kullanabilirsiniz)--

with cte as
(
select Cust_ID, Customer_name, order_date, lead(Order_Date, 1) OVER(PARTITION BY Cust_ID Order BY Order_Date ASC) as second_purchasing 
from dbo.e_commerce_data
),
cte2 as
(
select *, datediff(m, order_date, second_purchasing) AS elapsed_time from cte 
)

select datename(m, order_date) as [months],
	count(distinct Cust_ID) as count_month_customer 
	from cte2  
	where elapsed_time <= 3 
	group by (datename(m, order_date))
	order by count_month_customer



--2.Calculate the month-wise retention rate.
--Month-Wise Retention Rate = 1.0 * Number of Customers Retained in The Current Month / Total Number of Customers in the Current Month--
--(Y�ll�k elde tutma oran�n� hesaplay�n. 
--Ayl�k Elde Tutma Oran� = 1,0 * ��inde Bulunulan Ayda Elde Tutulan M��teri Say�s� / Toplam Cari Aydaki M��teri Say�s�)--

-- Number of Customers Retained by months--
with cte as
(
select Cust_ID, Customer_name, order_date, lead(Order_Date, 1) OVER(PARTITION BY Cust_ID Order BY Order_Date ASC) as second_purchasing 
from dbo.e_commerce_data
),
cte2 as
(
select *, datediff(m, order_date, second_purchasing) AS elapsed_time from cte 
),
cte3 as
(
select datename(m, order_date) as [Months], count(distinct Cust_ID) as count_month_customer from cte2 where elapsed_time <= 3 group by (datename(m, order_date))
),


--Total customer count by months--
cte4 as
(
select datename(m, order_date) AS [Months], count(distinct Cust_ID) as count_total_customer from dbo.e_commerce_data 
group by datename(m, order_date)
)

--Now I must divide this results according to months.
select cte3.Months,
Round(CAST(1.0 * count_month_customer/count_total_customer AS float), 3) As Retention_Rate 
from cte3 join cte4 ON cte3.Months = cte4.Months;

