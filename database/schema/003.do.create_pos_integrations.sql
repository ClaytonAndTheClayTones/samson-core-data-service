create table if not exists pos_integrations (
	id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
	name varchar(255) NOT NULL,
	description text NULL,
	pos_platform varchar(32) NOT NULL,
	created_at timestamptz(3) NOT NULL DEFAULT now(),
	updated_at timestamptz(3) 
);

CREATE INDEX IF NOT EXISTS idx_pos_integrations_name ON public.pos_integrations(name);  
CREATE INDEX IF NOT EXISTS idx_pos_integrations_pos_platform ON public.pos_integrations(pos_platform);   
CREATE INDEX IF NOT EXISTS idx_pos_integrations_created_at ON public.pos_integrations(created_at); 

ALTER TABLE public.pos_integrations DROP CONSTRAINT IF EXISTS enum_pos_integrations_pos_platform;
  
ALTER TABLE public.pos_integrations  
   ADD CONSTRAINT enum_pos_integrations_pos_platform 
   CHECK (pos_platform IN ('Posabit', 'Flowhub', 'Dutchie', 'KlickTrack', 'Cova', 'Meadow', 'GrowFlow', 'Unknown') );