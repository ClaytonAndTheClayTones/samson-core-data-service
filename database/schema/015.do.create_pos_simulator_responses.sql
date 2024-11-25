create table if not exists pos_simulator_responses (
	id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),   
   action_type varchar(32) NOT NULL, 
   response_body json NOT NULL,
   response_status_code integer NOT NULL, 
   description text NULL,
	created_at timestamptz(3) NOT NULL DEFAULT now(),
	updated_at timestamptz(3) 
);
  
CREATE INDEX IF NOT EXISTS idx_pos_simulator_responses_created_at ON public.pos_simulator_responses(created_at);
 
-- Enums
  
ALTER TABLE public.pos_simulator_responses DROP CONSTRAINT IF EXISTS enum_pos_simulator_responses_action_type;
  
ALTER TABLE public.pos_simulator_responses  
   ADD CONSTRAINT enum_pos_simulator_responses_action_type
   CHECK (action_type IN ('GetHistoricalSales', 'GetInventorySnapshots') );