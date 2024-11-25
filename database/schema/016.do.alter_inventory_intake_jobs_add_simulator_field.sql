alter table inventory_intake_jobs add column if not exists simulator_response_id uuid NULL;
 
  
CREATE INDEX IF NOT EXISTS idx_inventory_intake_jobs_simulator_response_id ON public.inventory_intake_jobs(simulator_response_id);

   
ALTER TABLE public.inventory_intake_jobs DROP CONSTRAINT IF EXISTS fk_inventory_intake_jobs_simulator_response_id;

ALTER TABLE public.inventory_intake_jobs
  ADD CONSTRAINT fk_inventory_intake_jobs_simulator_response_id
  FOREIGN KEY (simulator_response_id)
  REFERENCES public.pos_simulator_responses(id)
  On Delete Set Null;
