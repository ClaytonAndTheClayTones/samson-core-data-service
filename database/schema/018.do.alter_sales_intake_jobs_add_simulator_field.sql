alter table sales_intake_jobs add column if not exists simulator_response_id uuid NULL;
 
  
CREATE INDEX IF NOT EXISTS idx_sales_intake_jobs_simulator_response_id ON public.sales_intake_jobs(simulator_response_id);

   
ALTER TABLE public.sales_intake_jobs DROP CONSTRAINT IF EXISTS fk_sales_intake_jobs_simulator_response_id;

ALTER TABLE public.sales_intake_jobs
  ADD CONSTRAINT fk_sales_intake_jobs_simulator_response_id
  FOREIGN KEY (simulator_response_id)
  REFERENCES public.pos_simulator_responses(id)
  On Delete Set Null;
