create table if not exists inventory_intake_jobs (
	id uuid PRIMARY KEY DEFAULT uuid_generate_v4(), 
	retailer_id uuid NOT NULL, 
	retailer_location_id uuid NOT NULL,  
  snapshot_hour  timestamptz(3 )NOT NULL,   
  status  varchar(32) NOT NULL DEFAULT 'Requested',
  status_details json NOT NULL DEFAULT '{}',
	created_at timestamptz(3) NOT NULL DEFAULT now(),
	updated_at timestamptz(3) 
);
 
CREATE INDEX IF NOT EXISTS idx_inventory_intake_jobs_retailer_id ON public.inventory_intake_jobs(retailer_id);   
CREATE INDEX IF NOT EXISTS idx_inventory_intake_jobs_retailer_location_id ON public.inventory_intake_jobs(retailer_location_id);  
CREATE INDEX IF NOT EXISTS idx_inventory_intake_jobs_snapshot_hour ON public.inventory_intake_jobs(snapshot_hour);
CREATE INDEX IF NOT EXISTS idx_inventory_intake_jobs_status ON public.inventory_intake_jobs(status); 

-- Enums

ALTER TABLE public.inventory_intake_jobs DROP CONSTRAINT IF EXISTS enum_inventory_intake_jobs_status;
  
ALTER TABLE public.inventory_intake_jobs  
   ADD CONSTRAINT enum_inventory_intake_jobs_status 
   CHECK (status IN ('Requested', 'Processing', 'Failed', 'Complete') );
 
 
-- FKs
 

ALTER TABLE public.inventory_intake_jobs DROP CONSTRAINT IF EXISTS fk_inventory_intake_jobs_retailer_id;

ALTER TABLE public.inventory_intake_jobs
  ADD CONSTRAINT fk_inventory_intake_jobs_retailer_id
  FOREIGN KEY (retailer_id)
  REFERENCES public.retailers(id);

ALTER TABLE public.inventory_intake_jobs DROP CONSTRAINT IF EXISTS fk_inventory_intake_jobs_retailer_location_id;

ALTER TABLE public.inventory_intake_jobs
  ADD CONSTRAINT fk_inventory_intake_jobs_retailer_location_id
  FOREIGN KEY (retailer_location_id)
  REFERENCES public.retailer_locations(id); 