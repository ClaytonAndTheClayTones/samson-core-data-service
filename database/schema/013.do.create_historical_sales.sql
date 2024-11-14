create table if not exists historical_sales (
	id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),  
  pos_sale_id varchar(255) NOT NULL,
  sale_timestamp timestamptz(3) NOT NULL, 
	retailer_id uuid NOT NULL, 
	retailer_location_id uuid NOT NULL, 
  sales_intake_job_id uuid NULL,
  sub_total integer   NULL,
  discount integer   NULL,
  tax integer   NULL,
  total integer NOT NULL, 
  cost integer   NULL,
	created_at timestamptz(3) NOT NULL DEFAULT now(),
	updated_at timestamptz(3) 
);

CREATE INDEX IF NOT EXISTS idx_historical_sales_sales_intake_job_id ON public.historical_sales(sales_intake_job_id);   
CREATE INDEX IF NOT EXISTS idx_historical_sales_pos_sale_id ON public.historical_sales(pos_sale_id);   
CREATE INDEX IF NOT EXISTS idx_historical_sales_retailer_id ON public.historical_sales(retailer_id);   
CREATE INDEX IF NOT EXISTS idx_historical_sales_retailer_location_id ON public.historical_sales(retailer_location_id);
CREATE INDEX IF NOT EXISTS idx_historical_sales_sale_timestamp ON public.historical_sales(sale_timestamp); 
CREATE INDEX IF NOT EXISTS idx_historical_sales_created_at ON public.historical_sales(created_at); 
 
-- FKs
 

ALTER TABLE public.historical_sales DROP CONSTRAINT IF EXISTS fk_historical_sales_retailer_id;

ALTER TABLE public.historical_sales
  ADD CONSTRAINT fk_historical_sales_retailer_id
  FOREIGN KEY (retailer_id)
  REFERENCES public.retailers(id);

ALTER TABLE public.historical_sales DROP CONSTRAINT IF EXISTS fk_historical_sales_retailer_location_id;

ALTER TABLE public.historical_sales
  ADD CONSTRAINT fk_historical_sales_retailer_location_id
  FOREIGN KEY (retailer_location_id)
  REFERENCES public.retailer_locations(id);
 
ALTER TABLE public.historical_sales DROP CONSTRAINT IF EXISTS fk_historical_sales_sales_intake_job_id;

ALTER TABLE public.historical_sales
  ADD CONSTRAINT fk_historical_sales_sales_intake_job_id
  FOREIGN KEY (sales_intake_job_id)
  REFERENCES public.sales_intake_jobs(id);