create table if not exists pos_integration_calls (
	id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
	pos_integration_id uuid NOT NULL,
	retailer_location_id uuid NOT NULL,
	retailer_id uuid NOT NULL,
	request json NOT NULL,
	response json NULL,
	created_at timestamptz(3) NOT NULL DEFAULT now(),
	updated_at timestamptz(3) 
);

CREATE INDEX IF NOT EXISTS idx_pos_integration_calls_name ON public.pos_integration_calls(pos_integration_id);  
CREATE INDEX IF NOT EXISTS idx_pos_integration_calls_pos_platform ON public.pos_integration_calls(retailer_location_id);   
CREATE INDEX IF NOT EXISTS idx_pos_integration_calls_pos_platform ON public.pos_integration_calls(retailer_id);   
CREATE INDEX IF NOT EXISTS idx_pos_integration_calls_created_at ON public.pos_integration_calls(created_at); 