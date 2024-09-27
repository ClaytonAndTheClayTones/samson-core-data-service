create table if not exists retailer_locations (
	id uuid PRIMARY KEY DEFAULT uuid_generate_v4(), 
	retailer_id uuid NOT NULL,
  pos_integration_id uuid NULL,
	name varchar(255) NOT NULL,     
	location_city  varchar(255) NULL,
  location_state varchar(255) NULL,
  location_country varchar(2),
  contact_email varchar(320) NULL, 
  contact_phone varchar(32) NULL, 
	created_at timestamptz(3) NOT NULL DEFAULT now(),
	updated_at timestamptz(3) 
);

CREATE INDEX IF NOT EXISTS idx_retailer_locations_name ON public.retailer_locations(name);  
CREATE INDEX IF NOT EXISTS idx_retailer_locations_retailer_id ON public.retailer_locations(retailer_id);  
CREATE INDEX IF NOT EXISTS idx_retailer_locations_pos_integration_id ON public.retailer_locations(pos_integration_id);  
CREATE INDEX IF NOT EXISTS idx_retailer_locations_location_city ON public.retailer_locations(location_city); 
CREATE INDEX IF NOT EXISTS idx_retailer_locations_location_state ON public.retailer_locations(location_state); 
CREATE INDEX IF NOT EXISTS idx_retailer_locations_location_country ON public.retailer_locations(location_country); 
CREATE INDEX IF NOT EXISTS idx_retailer_locations_created_at ON public.retailer_locations(created_at); 
 
ALTER TABLE public.retailer_locations DROP CONSTRAINT IF EXISTS fk_retailer_locations_retailer_id;

ALTER TABLE public.retailer_locations
  ADD CONSTRAINT fk_retailer_locations_retailer_id
  FOREIGN KEY (retailer_id)
  REFERENCES public.retailers(id);