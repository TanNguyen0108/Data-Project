Use HCM_FOODSTORE_DATABASE
Go

CREATE TABLE DIM_SHOPEE_BRAND(
	brand_id INT PRIMARY KEY,
	brand_url VARCHAR(255),
	brand_name TEXT,
	restaurant_count INT
);
GO

BULK INSERT DIM_SHOPEE_BRAND
FROM 'C:\Users\tanguyen\Downloads\Data for Web Crawling\DIM_SHOPEE_BRAND.txt'
WITH(
	FIRSTROW = 2,
	FIELDTERMINATOR = '\t',
	ROWTERMINATOR = '\n'
)
GO

CREATE TABLE RESTAURANT(
	restaurant_id FLOAT,
	restaurant_url TEXT,
	restaurant_name TEXT,
	name_en TEXT,
	restaurant_short_description TEXT,
	address_detail TEXT,
	address_district TEXT,
	address_city TEXT,
	address_full TEXT,
	lat DECIMAL(9,6),
	lon DECIMAL(9,6),
	district_type TEXT,
	brand_id INT,
	delivery_avg_price INT,
	delivery_fees TEXT,
	delivery_has_contract INT,
	delivery_id INT,
	delivery_merchant_limit_distance INT,
	delivery_merchant_time INT,
	delivery_payment_methods TEXT,
	delivery_prepare_duration TEXT,
	PRIMARY KEY(restaurant_id),
	FOREIGN KEY (brand_id) REFERENCES DIM_SHOPEE_BRAND(brand_id) ON DELETE CASCADE ON UPDATE CASCADE
);
GO
--CHANGE TYPE

GO
ALTER TABLE RESTAURANT ALTER COLUMN lat DECIMAL(9,6)
ALTER TABLE RESTAURANT ALTER COLUMN lon DECIMAL(9,6)
ALTER TABLE RESTAURANT ALTER COLUMN delivery_avg_price INT
ALTER TABLE RESTAURANT ALTER COLUMN delivery_has_contract INT
ALTER TABLE RESTAURANT ALTER COLUMN delivery_id INT
ALTER TABLE RESTAURANT ALTER COLUMN delivery_merchant_limit_distance INT
ALTER TABLE RESTAURANT ALTER COLUMN delivery_merchant_time INT
ALTER TABLE RESTAURANT ALTER COLUMN delivery_prepare_duration INT
ALTER TABLE RESTAURANT ALTER COLUMN brand_id INT

GO


BULK INSERT RESTAURANT
FROM 'C:\Users\tanguyen\Downloads\Data for Web Crawling\RESTAURANT-bytab-cleansed.txt'
WITH(
	FIRSTROW = 2,
	FIELDTERMINATOR = '\t',
	ROWTERMINATOR ='\n'
)
GO

--Create Table hold data for DIM_ACTIVE_HOURS path: 'C:\Users\tanguyen\Downloads\Data for Web Crawling\DIM_ACTIVE_HOURS.csv'
CREATE TABLE DIM_ACTIVE_HOURS(
	restaurant_id FLOAT NULL,
	week_day INT,
	active_hour	INT
	FOREIGN KEY (restaurant_id) REFERENCES RESTAURANT(restaurant_id) ON DELETE CASCADE ON UPDATE CASCADE
);
GO
	--Bulk Import csv DIM_ACTIVE_HOURS
BULK INSERT DIM_ACTIVE_HOURS
FROM 'C:\Users\tanguyen\Downloads\Data for Web Crawling\DIM_ACTIVE_HOURS.csv'
WITH (
	FIRSTROW = 2,
	FIELDTERMINATOR = ',',
	ROWTERMINATOR = '\n'
);
GO

--Create Table hold data for DIM_FOODY_AUDIENCE path: 'C:\Users\tanguyen\Downloads\Data for Web Crawling\DIM_FOODY_AUDIENCE.csv'
CREATE TABLE DIM_FOODY_AUDIENCE(
	restaurant_id FLOAT NULL,
	audience TEXT
	FOREIGN KEY (restaurant_id) REFERENCES RESTAURANT(restaurant_id) ON DELETE CASCADE ON UPDATE CASCADE
);
GO
	--BULK IMPORT
BULK INSERT DIM_FOODY_AUDIENCE
FROM 'C:\Users\tanguyen\Downloads\Data for Web Crawling\DIM_FOODY_AUDIENCE.csv'
WITH (
	FIRSTROW = 2,
	FIELDTERMINATOR = ',',
	ROWTERMINATOR = '\n'
)
GO

CREATE TABLE DIM_FOODY_CATEGORY(
	restaurant_id FLOAT NULL,
	category VARCHAR(255)
	FOREIGN KEY (restaurant_id) REFERENCES RESTAURANT(restaurant_id) ON DELETE CASCADE ON UPDATE CASCADE
);

BULK INSERT DIM_FOODY_CATEGORY
FROM 'C:\Users\tanguyen\Downloads\Data for Web Crawling\DIM_FOODY_CATEGORY.csv'
WITH(
	FIRSTROW = 2,
	FIELDTERMINATOR = ',',
	ROWTERMINATOR = '\n'
)
GO


CREATE TABLE DIM_FOODY_CUISINE(
	restaurant_id FLOAT NULL,
	cuisine VARCHAR(255),
	FOREIGN KEY (restaurant_id) REFERENCES RESTAURANT(restaurant_id) ON DELETE CASCADE ON UPDATE CASCADE
);

BULK INSERT DIM_FOODY_CUISINE
FROM 'C:\Users\tanguyen\Downloads\Data for Web Crawling\DIM_FOODY_CUISINE.csv'
WITH(
	FIRSTROW = 2,
	FIELDTERMINATOR = ',',
	ROWTERMINATOR = '\n'
)
GO



-- DROP TABLE

DROP TABLE IF EXISTS DIM_FOODY_AUDIENCE;
DROP TABLE IF EXISTS DIM_ACTIVE_HOURS;
DROP TABLE IF EXISTS DIM_FOODY_CATEGORY;
DROP TABLE IF EXISTS DIM_FOODY_CUISINE;

DROP TABLE IF EXISTS RESTAURANT;

DROP TABLE IF EXISTS DIM_SHOPEE_BRAND;

DROP TABLE IF EXISTS DIM_SHOPEE_DISHES;




DROP TABLE IF EXISTS DIM_SHOPEE_DISHES;
CREATE TABLE DIM_SHOPEE_DISHES(
	catalog_id INT,
	dish_total_order TEXT,
	catalog_name TEXT,
	catalog_rank TEXT,
	catalog_partner_catalog_id TEXT,
	catalog_description TEXT,
	dish_restaurant_id FLOAT NULL,
	dish_id TEXT,
	dish_name TEXT,
	dish_partner_dish_id TEXT,
	dish_listing_status TEXT,
	dish_description TEXT,
	dish_total_like TEXT,
	dish_rank TEXT,
	dish_picture_label TEXT,
	dish_is_hidden TEXT,
	dish_price text,
	dish_is_group_discount_item TEXT,
	dishes_property_info TEXT,
	url TEXT,
	FOREIGN KEY (dish_restaurant_id) REFERENCES RESTAURANT(restaurant_id) ON DELETE CASCADE ON UPDATE CASCADE
);
GO

BULK INSERT DIM_SHOPEE_DISHES
FROM 'C:\Users\tanguyen\Downloads\Data for Web Crawling\DIM_SHOPEE_DISHES_sp4.csv'
WITH(
	FIRSTROW = 2,
	FIELDTERMINATOR = '|',
	ROWTERMINATOR = '\n'
)
GO