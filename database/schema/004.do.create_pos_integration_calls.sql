create table if not exists pos_integration_calls (
	id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
	retailer_id uuid NOT NULL,
	retailer_location_id uuid NOT NULL,
	pos_integration_id uuid NOT NULL,
	request json NOT NULL,
	response_status_code integer NOT NULL,
	response json NULL,
	created_at timestamptz(3) NOT NULL DEFAULT now(),
	updated_at timestamptz(3) 
);

CREATE INDEX IF NOT EXISTS idx_pos_integration_calls_pos_integration_id ON public.pos_integration_calls(pos_integration_id);  
CREATE INDEX IF NOT EXISTS idx_pos_integration_calls_retailer_location_id ON public.pos_integration_calls(retailer_location_id);   
CREATE INDEX IF NOT EXISTS idx_pos_integration_calls_retailer_id ON public.pos_integration_calls(retailer_id);   
CREATE INDEX IF NOT EXISTS idx_pos_integration_calls_response_status_code ON public.pos_integration_calls(response_status_code);   
CREATE INDEX IF NOT EXISTS idx_pos_integration_calls_created_at ON public.pos_integration_calls(created_at); 

-- FKs

ALTER TABLE public.pos_integration_calls DROP CONSTRAINT IF EXISTS fk_pos_integration_calls_retailer_location_id;

ALTER TABLE public.pos_integration_calls
  ADD CONSTRAINT fk_pos_integration_calls_retailer_location_id
  FOREIGN KEY (retailer_location_id)
  REFERENCES public.retailer_locations(id)
  ON DELETE SET NULL;

ALTER TABLE public.pos_integration_calls DROP CONSTRAINT IF EXISTS fk_pos_integration_calls_retailer_id;

ALTER TABLE public.pos_integration_calls
  ADD CONSTRAINT fk_pos_integration_calls_retailer_id
  FOREIGN KEY (retailer_id)
  REFERENCES public.retailers(id)
  ON DELETE SET NULL;

ALTER TABLE public.pos_integration_calls DROP CONSTRAINT IF EXISTS fk_pos_integration_calls_pos_integration_id;

ALTER TABLE public.pos_integration_calls
  ADD CONSTRAINT fk_pos_integration_calls_pos_integration_id
  FOREIGN KEY (pos_integration_id)
  REFERENCES public.pos_integrations(id)
  ON DELETE SET NULL;