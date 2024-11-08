create table if not exists inventory_intake_batch_jobs (
	id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),  
  start_time  timestamptz(3) NOT NULL,   
  end_time  timestamptz(3) NOT NULL DEFAULT now(),   
  restricted_retailer_location_ids  text NULL,
  status  varchar(32) NOT NULL DEFAULT 'Requested',
  status_details json NOT NULL DEFAULT '{}',
	created_at timestamptz(3) NOT NULL DEFAULT now(),
	updated_at timestamptz(3) 
);
  
CREATE INDEX IF NOT EXISTS idx_inventory_intake_batch_jobs_start_time ON public.inventory_intake_batch_jobs(start_time);
CREATE INDEX IF NOT EXISTS idx_inventory_intake_batch_jobs_end_time ON public.inventory_intake_batch_jobs(end_time);
CREATE INDEX IF NOT EXISTS idx_inventory_intake_batch_jobs_status ON public.inventory_intake_batch_jobs(status); 

-- Enums

ALTER TABLE public.inventory_intake_batch_jobs DROP CONSTRAINT IF EXISTS enum_inventory_intake_batch_jobs_status;
  
ALTER TABLE public.inventory_intake_batch_jobs  
   ADD CONSTRAINT enum_inventory_intake_batch_jobs_status 
   CHECK (status IN ('Requested', 'Processing', 'Failed', 'Complete') );
