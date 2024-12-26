create table if not exists historical_sale_items (
	id uuid PRIMARY KEY DEFAULT uuid_generate_v4(), 
	product_id uuid NOT NULL, 	
	product_vendor_id uuid NULL, 	
  retailer_id uuid NOT NULL, 
	retailer_location_id uuid NOT NULL, 
  sales_intake_job_id uuid NULL, 
  historical_sale_id uuid NOT NULL,

  pos_product_id varchar(255) NULL, 
  pos_sale_id varchar(255) NULL,

  sku varchar(255) NOT NULL,
  sale_count decimal(19,3) NOT NULL,

  sale_timestamp timestamptz(3) NOT NULL,  
 
  lot_identifier varchar(255) NULL,
  unit_of_weight varchar(255)   NULL,
  weight_in_units decimal(19,3)   NULL,

  sale_product_name varchar(255) NULL,  
  product_name varchar(255) NULL, 
  sub_total integer   NULL,
  discount integer   NULL,
  tax integer   NULL,
  total integer NOT NULL, 
  cost integer   NULL,

	created_at timestamptz(3) NOT NULL DEFAULT now(),
	updated_at timestamptz(3) 
);

CREATE INDEX IF NOT EXISTS idx_historical_sale_items_sales_intake_job_id ON public.historical_sale_items(sales_intake_job_id);   
CREATE INDEX IF NOT EXISTS idx_historical_sale_items_retailer_id ON public.historical_sale_items(retailer_id);   
CREATE INDEX IF NOT EXISTS idx_historical_sale_items_retailer_location_id ON public.historical_sale_items(retailer_location_id);
CREATE INDEX IF NOT EXISTS idx_historical_sale_items_product_id ON public.historical_sale_items(product_id);
CREATE INDEX IF NOT EXISTS idx_historical_sale_items_product_vendor_id ON public.historical_sale_items(product_vendor_id);

CREATE INDEX IF NOT EXISTS idx_historical_sale_items_historical_sale_id ON public.historical_sale_items(historical_sale_id);   
CREATE INDEX IF NOT EXISTS idx_historical_sale_items_historical_sale_id ON public.historical_sale_items(pos_product_id);

create index if not exists idx_historical_sale_items_sku ON public.historical_sale_items(sku);
CREATE INDEX IF NOT EXISTS idx_historical_sale_items_sale_timestamp ON public.historical_sale_items(sale_timestamp); 

Create index if not exists idx_historical_sale_items_sale_product_name ON public.historical_sale_items(sale_product_name); 
CREATE INDEX IF NOT EXISTS idx_historical_sale_items_created_at ON public.historical_sale_items(created_at); 
 
-- FKs
ALTER TABLE public.historical_sale_items DROP CONSTRAINT IF EXISTS fk_historical_sale_items_product_id;

ALTER TABLE public.historical_sale_items
  ADD CONSTRAINT fk_historical_sale_items_product_id
  FOREIGN KEY (product_id)
  REFERENCES public.products(id);

ALTER TABLE public.historical_sale_items DROP CONSTRAINT IF EXISTS fk_historical_sale_items_product_id;

ALTER TABLE public.historical_sale_items
  ADD CONSTRAINT fk_historical_sale_items_product_id
  FOREIGN KEY (product_id)
  REFERENCES public.products(id);

ALTER TABLE public.historical_sale_items DROP CONSTRAINT IF EXISTS fk_historical_sale_items_retailer_id;

ALTER TABLE public.historical_sale_items
  ADD CONSTRAINT fk_historical_sale_items_retailer_id
  FOREIGN KEY (retailer_id)
  REFERENCES public.retailers(id);

ALTER TABLE public.historical_sale_items DROP CONSTRAINT IF EXISTS fk_historical_sale_items_retailer_location_id;

ALTER TABLE public.historical_sale_items
  ADD CONSTRAINT fk_historical_sale_items_retailer_location_id
  FOREIGN KEY (retailer_location_id)
  REFERENCES public.retailer_locations(id);
 
ALTER TABLE public.historical_sale_items DROP CONSTRAINT IF EXISTS fk_historical_sale_items_sales_intake_job_id;

ALTER TABLE public.historical_sale_items
  ADD CONSTRAINT fk_historical_sale_items_sales_intake_job_id
  FOREIGN KEY (sales_intake_job_id)
  REFERENCES public.sales_intake_jobs(id);
 