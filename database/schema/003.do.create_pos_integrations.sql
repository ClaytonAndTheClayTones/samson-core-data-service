create table if not exists pos_integrations (
	id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
	retailer_id uuid NULL,
	retailer_location_id uuid NULL,
	name varchar(255) NOT NULL,
	url text NOT NULL,
	key varchar(255) NOT NULL,
	description text NULL,
	pos_platform varchar(32) NOT NULL,
	created_at timestamptz(3) NOT NULL DEFAULT now(),
	updated_at timestamptz(3) 
);

CREATE INDEX IF NOT EXISTS idx_pos_integrations_name ON public.pos_integrations(name);  
CREATE INDEX IF NOT EXISTS idx_pos_integrations_pos_platform ON public.pos_integrations(pos_platform);   
CREATE INDEX IF NOT EXISTS idx_pos_integrations_retailer_id ON public.pos_integrations(retailer_id);  
CREATE INDEX IF NOT EXISTS idx_pos_integrations_retailer_location_id ON public.pos_integrations(retailer_location_id);  
CREATE INDEX IF NOT EXISTS idx_pos_integrations_created_at ON public.pos_integrations(created_at); 

-- Enums

ALTER TABLE public.pos_integrations DROP CONSTRAINT IF EXISTS enum_pos_integrations_pos_platform;
  
ALTER TABLE public.pos_integrations  
   ADD CONSTRAINT enum_pos_integrations_pos_platform 
   CHECK (pos_platform IN ('Posabit', 'Flowhub', 'Dutchie', 'KlickTrack', 'Cova', 'Meadow', 'GrowFlow', 'Unknown') );

-- FKs

ALTER TABLE public.pos_integrations DROP CONSTRAINT IF EXISTS fk_pos_integrations_retailer_location_id;

ALTER TABLE public.pos_integrations
  ADD CONSTRAINT fk_pos_integrations_retailer_location_id
  FOREIGN KEY (retailer_location_id)
  REFERENCES public.retailer_locations(id)
  ON DELETE SET NULL;

ALTER TABLE public.pos_integrations DROP CONSTRAINT IF EXISTS fk_pos_integrations_retailer_id;

ALTER TABLE public.pos_integrations
  ADD CONSTRAINT fk_pos_integrations_retailer_id
  FOREIGN KEY (retailer_id)
  REFERENCES public.retailers(id)
  ON DELETE SET NULL;